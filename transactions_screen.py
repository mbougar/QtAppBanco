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

        # Create the main layout
        main_layout = QVBoxLayout(self)

        # Create a frame to hold all the content
        self.mainFrame = QFrame(self)
        self.mainFrame.setObjectName("mainFrame")

        layout = QVBoxLayout(self.mainFrame)

        ##Title frame
        self.titleFrame = QFrame(self.mainFrame)
        self.titleFrame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(self.titleFrame)
        title_layout.addWidget(TitleLabel("Transacciones"))
        layout.addWidget(self.titleFrame)

        ##Filters frame
        self.filtersFrame = QFrame(self.mainFrame)
        self.filtersFrame.setObjectName("filtersFrame")
        filter_layout = QHBoxLayout(self.filtersFrame)
        self.start_date = CalendarPicker()
        self.end_date = CalendarPicker()
        self.filter_button = PrimaryPushButton("Filtrar")
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(self.end_date)
        filter_layout.addWidget(self.filter_button)
        layout.addWidget(self.filtersFrame)

        self.start_date.date = QDate.fromString("01/01/1990", "dd/M/yyyy")
        self.end_date.date = QDate.currentDate()

        ##TransactionsFrame
        self.transactionsFrame = QFrame(self.mainFrame)
        self.transactionsFrame.setObjectName("transactionsFrame")
        transaction_layout = QHBoxLayout(self.transactionsFrame)

        ## TransactionTable
        self.transactionTableView = TableWidget(self)
        self.transactionTableView.setBorderVisible(True)
        self.transactionTableView.setBorderRadius(8)

        self.transactionTableView.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.transactionTableView.setWordWrap(False)
        self.transactionTableView.setColumnCount(3)

        # Obtener transacciones de la base de datos
        transactions = LocalDbConn.obtenerTodastransaccionesDeUsuario()

        # Ajusta las filas para que sean el numero de la lista
        self.transactionTableView.setRowCount(len(transactions))

        # Bucle para poblar la tabla con las transacciones
        for i, transaction in enumerate(transactions):
            fecha = transaction[5].split(" ")[0]
            cantidad = transaction[2]
            descripcion = transaction[4]

            # Asigna los valores a las celdas correspondientes
            self.transactionTableView.setItem(i, 0, QTableWidgetItem(fecha))
            self.transactionTableView.setItem(i, 1, QTableWidgetItem(str(cantidad) + "€"))
            self.transactionTableView.setItem(i, 2, QTableWidgetItem(descripcion))

        self.transactionTableView.verticalHeader().hide()
        self.transactionTableView.resizeColumnsToContents()
        self.transactionTableView.setHorizontalHeaderLabels(["Fecha", "Cantidad", "Desc"])
        self.transactionTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        transaction_layout.addWidget(self.transactionTableView)
        layout.addWidget(self.transactionsFrame)
        self.filter_button.clicked.connect(self.filter_transactions)
        #self.filter_transactions()

        self.mainFrame.setStyleSheet("""
            #mainFrame {
                background-color: #3a6d91;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        self.titleFrame.setStyleSheet("""
            #titleFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        self.filtersFrame.setStyleSheet("""
            #filtersFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        self.transactionsFrame.setStyleSheet("""
            #transactionsFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        main_layout.addWidget(self.mainFrame)

    def filter_transactions(self):
        start_date = self.start_date.date
        end_date = self.end_date.date

        if (start_date > end_date):
            self.showMessageBox()

        for row in range(self.transactionTableView.rowCount()):
            date_item = self.transactionTableView.item(row, 0)
            if date_item:
                try:
                    transaction_date = QDate.fromString(date_item.text(), "dd/M/yyyy")

                    #Comprobamos si la transaccion esta en el rango de fechas
                    if start_date <= transaction_date <= end_date:
                        self.transactionTableView.setRowHidden(row, False)
                    else:
                        self.transactionTableView.setRowHidden(row, True)
                except Exception as e:
                    print(e)

    def showMessageBox(self):
        message = MessageBox(
            "Alerta",
            "La fecha final que ha seleccionado es anterior a la fecha de inicio. ¿Desea restablecer las fechas a sus valores por defecto?",
            self
        )
        message.yesButton.setText("Aceptar")
        message.cancelButton.setText("Cancelar")

        if message.exec():
            self.end_date.date = QDate.currentDate()
            self.start_date.date = QDate.fromString("01/01/1990", "dd/M/yyyy")
            self.filter_transactions()
