import sys
from PyQt6.QtCore import Qt, QDate, QSize, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QDateEdit, QFrame
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, FluentIcon as FIF, setTheme, Theme
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QHeaderView
from qfluentwidgets import TableWidget, setTheme, Theme, FluentIconBase, StrongBodyLabel, TitleLabel, PixmapLabel, CalendarPicker, PrimaryPushButton, PushButton, MessageBox
from local_db_con import LocalDbConn
from datetime import datetime


class TransactionsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("transactionsScreen")

        # Crear el layout principal
        main_layout = QVBoxLayout(self)

        # Crear un marco (frame) para contener todo el contenido
        self.mainFrame = QFrame(self)
        self.mainFrame.setObjectName("mainFrame")

        layout = QVBoxLayout(self.mainFrame)

        ## Marco del título
        self.titleFrame = QFrame(self.mainFrame)
        self.titleFrame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(self.titleFrame)
        title_layout.addWidget(TitleLabel("Transacciones"))
        layout.addWidget(self.titleFrame)

        ## Marco de filtros
        self.filtersFrame = QFrame(self.mainFrame)
        self.filtersFrame.setObjectName("filtersFrame")
        filter_layout = QHBoxLayout(self.filtersFrame)
        self.start_date = CalendarPicker()  # Selector de fecha de inicio
        self.end_date = CalendarPicker()  # Selector de fecha de fin
        self.filter_button = PrimaryPushButton("Filtrar")  # Botón para aplicar los filtros
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(self.end_date)
        filter_layout.addWidget(self.filter_button)
        layout.addWidget(self.filtersFrame)

        # Establecer las fechas predeterminadas para los filtros
        self.start_date.date = QDate.fromString("01/01/1990", "dd/M/yyyy")
        self.end_date.date = QDate.currentDate()

        ## Marco de transacciones
        self.transactionsFrame = QFrame(self.mainFrame)
        self.transactionsFrame.setObjectName("transactionsFrame")
        transaction_layout = QHBoxLayout(self.transactionsFrame)

        ## Tabla de transacciones
        self.transactionTableView = TableWidget(self)
        self.transactionTableView.setBorderVisible(True)
        self.transactionTableView.setBorderRadius(8)

        # Desactivar la edición de las celdas
        self.transactionTableView.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Ajustar el ajuste de palabras y el número de columnas
        self.transactionTableView.setWordWrap(False)
        self.transactionTableView.setColumnCount(3)

        # Obtener las transacciones desde la base de datos
        transactions = LocalDbConn.obtenerTodastransaccionesDeUsuario()

        # Ajustar el número de filas según la cantidad de transacciones
        self.transactionTableView.setRowCount(len(transactions))

        # Llenar la tabla con las transacciones obtenidas
        for i, transaction in enumerate(transactions):
            fecha = transaction[5].split(" ")[0]  # Extraer solo la fecha
            cantidad = transaction[2]  # Monto de la transacción
            descripcion = transaction[4]  # Descripción de la transacción

            # Asignar los valores a las celdas correspondientes en la tabla
            self.transactionTableView.setItem(i, 0, QTableWidgetItem(fecha))
            self.transactionTableView.setItem(i, 1, QTableWidgetItem(str(cantidad) + "€"))
            self.transactionTableView.setItem(i, 2, QTableWidgetItem(descripcion))

        # Ocultar el encabezado vertical y ajustar el tamaño de las columnas
        self.transactionTableView.verticalHeader().hide()
        self.transactionTableView.resizeColumnsToContents()
        self.transactionTableView.setHorizontalHeaderLabels(["Fecha", "Cantidad", "Desc"])
        self.transactionTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Añadir la tabla al layout de transacciones
        transaction_layout.addWidget(self.transactionTableView)
        layout.addWidget(self.transactionsFrame)

        # Conectar el botón de filtro con la función para aplicar los filtros
        self.filter_button.clicked.connect(self.filter_transactions)

        # Aplicar estilo CSS al marco principal
        self.mainFrame.setStyleSheet("""
            #mainFrame {
                background-color: #3a6d91;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # Estilo del marco del título
        self.titleFrame.setStyleSheet("""
            #titleFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # Estilo del marco de filtros
        self.filtersFrame.setStyleSheet("""
            #filtersFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # Estilo del marco de transacciones
        self.transactionsFrame.setStyleSheet("""
            #transactionsFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # Añadir el marco principal al layout
        main_layout.addWidget(self.mainFrame)

    def filter_transactions(self):
        # Obtener las fechas de inicio y fin seleccionadas
        start_date = self.start_date.date
        end_date = self.end_date.date

        # Si la fecha de inicio es posterior a la de fin, mostrar un mensaje de error
        if (start_date > end_date):
            self.showMessageBox()

        # Filtrar las transacciones según las fechas seleccionadas
        for row in range(self.transactionTableView.rowCount()):
            date_item = self.transactionTableView.item(row, 0)
            print(date_item)
            if date_item:
                try:
                    # Convertir la fecha de la transacción de la tabla a un objeto QDate
                    transaction_date = QDate.fromString(date_item.text(), "yyyy-MM-dd")
                    print(transaction_date)

                    # Comprobar si la transacción está dentro del rango de fechas
                    if start_date <= transaction_date <= end_date:
                        self.transactionTableView.setRowHidden(row, False)  # Mostrar la transacción
                        print("He entrado en el if")
                    else:
                        self.transactionTableView.setRowHidden(row, True)  # Ocultar la transacción
                        print("No he entrado en el if")
                except Exception as e:
                    print(e)

    def showMessageBox(self):
        # Crear y mostrar un cuadro de mensaje si las fechas no son válidas
        message = MessageBox(
            "Alerta",
            "La fecha final que ha seleccionado es anterior a la fecha de inicio. ¿Desea restablecer las fechas a sus valores por defecto?",
            self
        )
        message.yesButton.setText("Aceptar")
        message.cancelButton.setText("Cancelar")

        # Si el usuario acepta, restablecer las fechas a los valores por defecto
        if message.exec():
            self.end_date.date = QDate.currentDate()
            self.start_date.date = QDate.fromString("01/01/1990", "dd/M/yyyy")
            self.filter_transactions()  # Aplicar los filtros de nuevo
