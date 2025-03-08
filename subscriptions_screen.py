import sys
from PyQt6.QtCore import Qt, QDate, QSize, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QDateEdit, QFrame
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, FluentIcon as FIF, setTheme, Theme
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QHeaderView
from qfluentwidgets import TableWidget, setTheme, Theme, FluentIconBase, StrongBodyLabel, TitleLabel, PixmapLabel, LineEdit, PrimaryPushButton, MessageBox
from local_db_con import LocalDbConn
from datetime import datetime

class SubscriptionsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("subscriptionsScreen")
        
        # Create the main layout
        main_layout = QVBoxLayout(self)

        # mainFrame
        self.mainFrame = QFrame(self)
        self.mainFrame.setObjectName("mainFrame")

        layout = QVBoxLayout(self.mainFrame)

        ##Title frame
        self.titleFrame = QFrame(self.mainFrame)
        self.titleFrame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(self.titleFrame)
        title_layout.addWidget(TitleLabel("Subscripciones"))
        layout.addWidget(self.titleFrame)

        ## Filters frame
        self.filtersFrame = QFrame(self.mainFrame)
        self.filtersFrame.setObjectName("filtersFrame")
        filter_layout = QHBoxLayout(self.filtersFrame)
        self.filter_line = LineEdit()
        self.filter_button = PrimaryPushButton("Filtrar")
        self.filter_line.setPlaceholderText("Filtrar por servicio")
        filter_layout.addWidget(self.filter_line)
        filter_layout.addWidget(self.filter_button)
        layout.addWidget(self.filtersFrame)

        # Subscriptions Frame

        self.subscriptionsFrame = QFrame(self.mainFrame)
        self.subscriptionsFrame.setObjectName("subscriptionsFrame")
        subcription_layout = QHBoxLayout(self.subscriptionsFrame)

        self.subscriptionTableView = TableWidget(self)
        self.subscriptionTableView.setBorderVisible(True)
        self.subscriptionTableView.setBorderRadius(8)

        self.subscriptionTableView.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.subscriptionTableView.setWordWrap(False)
        self.subscriptionTableView.setColumnCount(2)

        # obtener suscripciones de la bd
        suscriptions = LocalDbConn.obtenerTodasSuscripcionesDeUsuario()

        # ajusta las filas para que sean el numero de la lista
        self.subscriptionTableView.setRowCount(len(suscriptions))

        # Bucle para poblar la tabla con las suscripciones
        for i, suscription in enumerate(suscriptions):
            servicio = suscription[3]
            coste = suscription[2]
          
            # Añade los datos a la tabla
            self.subscriptionTableView.setItem(i, 0, QTableWidgetItem(str(servicio)))
            self.subscriptionTableView.setItem(i, 1, QTableWidgetItem(str(coste) + "€"))

        self.subscriptionTableView.verticalHeader().hide()
        self.subscriptionTableView.resizeColumnsToContents()
        self.subscriptionTableView.setHorizontalHeaderLabels(["Servicio", "Coste/mes"])
        self.subscriptionTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)        

        subcription_layout.addWidget(self.subscriptionTableView)
        layout.addWidget(self.subscriptionsFrame)
        self.filter_button.clicked.connect(self.filter_subscriptions)

        ##Stylesheet with all the styles for the frames and background

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

        main_layout.addWidget(self.mainFrame)
        


    def filter_subscriptions(self):

        # obtiene suscripciones con el filtro 

        filter = self.filter_line.text()

        for row in range(self.subscriptionTableView.rowCount()):
            serviceName = self.subscriptionTableView.item(row, 0)
            if serviceName:
                try:
                    
                    #Comprobamos si algun servicio contiene el filtro
                    if filter.lower() in serviceName.text().lower():
                        self.subscriptionTableView.setRowHidden(row, False)
                    else:
                        self.subscriptionTableView.setRowHidden(row, True)
                except Exception as e:
                    print(e)