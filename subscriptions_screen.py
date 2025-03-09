import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
from qfluentwidgets import TitleLabel, LineEdit, PrimaryPushButton, TableWidget
from local_db_con import LocalDbConn

class SubscriptionsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("subscriptionsScreen")
        
        # Layout principal de la pantalla
        main_layout = QVBoxLayout(self)

        # Marco principal que contiene todos los elementos
        self.mainFrame = QFrame(self)
        self.mainFrame.setObjectName("mainFrame")
        layout = QVBoxLayout(self.mainFrame)

        # Marco del título
        self.titleFrame = QFrame(self.mainFrame)
        self.titleFrame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(self.titleFrame)
        title_layout.addWidget(TitleLabel("Subscripciones"))
        layout.addWidget(self.titleFrame)

        # Marco de filtros
        self.filtersFrame = QFrame(self.mainFrame)
        self.filtersFrame.setObjectName("filtersFrame")
        filter_layout = QHBoxLayout(self.filtersFrame)
        self.filter_line = LineEdit()
        self.filter_button = PrimaryPushButton("Filtrar")
        self.filter_line.setPlaceholderText("Filtrar por servicio")
        filter_layout.addWidget(self.filter_line)
        filter_layout.addWidget(self.filter_button)
        layout.addWidget(self.filtersFrame)

        # Marco de suscripciones
        self.subscriptionsFrame = QFrame(self.mainFrame)
        self.subscriptionsFrame.setObjectName("subscriptionsFrame")
        subcription_layout = QHBoxLayout(self.subscriptionsFrame)

        # Tabla para mostrar las suscripciones
        self.subscriptionTableView = TableWidget(self)
        self.subscriptionTableView.setBorderVisible(True)
        self.subscriptionTableView.setBorderRadius(8)
        self.subscriptionTableView.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Evita que los datos sean editables
        self.subscriptionTableView.setWordWrap(False)
        self.subscriptionTableView.setColumnCount(2)  # Dos columnas: servicio y coste

        # Obtener suscripciones desde la base de datos
        suscriptions = LocalDbConn.obtenerTodasSuscripcionesDeUsuario()
        self.subscriptionTableView.setRowCount(len(suscriptions))  # Ajusta el número de filas según los datos obtenidos

        # Poblar la tabla con los datos de suscripciones
        for i, suscription in enumerate(suscriptions):
            servicio = suscription[3]  # Nombre del servicio
            coste = suscription[2]  # Coste mensual
            self.subscriptionTableView.setItem(i, 0, QTableWidgetItem(str(servicio)))
            self.subscriptionTableView.setItem(i, 1, QTableWidgetItem(str(coste) + "€"))

        # Configurar la tabla para mejorar la visualización
        self.subscriptionTableView.verticalHeader().hide()
        self.subscriptionTableView.resizeColumnsToContents()
        self.subscriptionTableView.setHorizontalHeaderLabels(["Servicio", "Coste/mes"])
        self.subscriptionTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Agregar la tabla al layout
        subcription_layout.addWidget(self.subscriptionTableView)
        layout.addWidget(self.subscriptionsFrame)

        # Conectar el botón de filtro con la función correspondiente
        self.filter_button.clicked.connect(self.filter_subscriptions)

        # Agregar estilos para los marcos
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

        self.subscriptionsFrame.setStyleSheet("""
            #subscriptionsFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # Agregar el marco principal al layout de la pantalla
        main_layout.addWidget(self.mainFrame)
        
    def filter_subscriptions(self):
        """ Filtra las suscripciones según el texto ingresado """
        filter_text = self.filter_line.text().lower()

        for row in range(self.subscriptionTableView.rowCount()):
            service_name = self.subscriptionTableView.item(row, 0)  # Obtiene el nombre del servicio
            if service_name:
                try:
                    # Verifica si el filtro está contenido en el nombre del servicio
                    if filter_text in service_name.text().lower():
                        self.subscriptionTableView.setRowHidden(row, False)
                    else:
                        self.subscriptionTableView.setRowHidden(row, True)
                except Exception as e:
                    print(e)