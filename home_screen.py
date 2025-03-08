import sys
from PyQt6.QtCore import Qt, QDate, QSize, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QDateEdit, QFrame
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, FluentIcon as FIF, setTheme, Theme
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QHeaderView
from qfluentwidgets import TableWidget, setTheme, Theme, FluentIconBase, StrongBodyLabel, TitleLabel
from local_db_con import LocalDbConn
from datetime import datetime

import utils

class HomeScreen(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setObjectName("homeScreen")

        main_layout = QVBoxLayout(self)

        # mainFrame
        self.mainFrame = QFrame(self)
        self.mainFrame.setObjectName("mainFrame")

        layout = QVBoxLayout(self.mainFrame)


        ##Header Frame
        self.headerFrame = QFrame(self.mainFrame)
        self.headerFrame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(self.headerFrame)
        header_layout.addWidget(TitleLabel(f"Hola {LocalDbConn.actualUser.nombre}, ¡Bienvenido de nuevo!"))
        layout.addWidget(self.headerFrame)

        # Cuentas (Maximo 3)

        self.accountsFrame = QFrame(self.mainFrame)
        self.accountsFrame.setObjectName("accountsFrame")

        accounts_layout = QHBoxLayout(self.accountsFrame)

        ## obtener las ultimas cuentas del usuario

        accounts = LocalDbConn.obtenerUltimasTresCuentasDeUsuario()

        ## Crea las tarjetitas arriba si tienes alguna cuenta
        for account in accounts:

            num = LocalDbConn.obtenerTarjetaDeCuenta(account[0])
        
            if num == None:
                toShow = "No tiene tarjeta asociada"
            elif num == []:
                toShow = "No tiene tarjeta asociada"
            else:
                toShow = num[0]

            card = self.create_account_card(str(account[3]) + "€", account[2], toShow )
            accounts_layout.addWidget(card)

        layout.addWidget(self.accountsFrame)

        ##Body Frame
        self.bodyFrame = QFrame(self.mainFrame)
        self.bodyFrame.setObjectName("bodyFrame")

        body_layout = QVBoxLayout(self.bodyFrame)

        # Tags con nombres de tablas
        tags = QHBoxLayout()
        self.transaction_label = StrongBodyLabel("Transacciones")
        self.subscription_label = StrongBodyLabel("Subscripciones")
        tags.addWidget(self.transaction_label)
        tags.addWidget(self.subscription_label)
        body_layout.addLayout(tags)

        # Transactions & Subscriptions
        content_layout = QHBoxLayout()

        # Transactions
        self.transactionTableView = TableWidget(self)
        self.transactionTableView.setBorderVisible(True)
        self.transactionTableView.setBorderRadius(8)

        self.transactionTableView.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.transactionTableView.setWordWrap(False)
        self.transactionTableView.setRowCount(4)
        self.transactionTableView.setColumnCount(3)

        # obtiene las ultimas 4 suscripciones de la bd

        transactions = LocalDbConn.obtenerUltimasCuatroTransaccionesDeUsuario()

        for i, transaction in enumerate(transactions):
            fecha = transaction[5].split(" ")[0]
            cantidad = transaction[2]
            descripcion = transaction[4]
          
            # Asigna los valores a las celdas correspondientes
            self.transactionTableView.setItem(i, 0, QTableWidgetItem(str(fecha)))
            self.transactionTableView.setItem(i, 1, QTableWidgetItem(str(cantidad) + "€"))
            self.transactionTableView.setItem(i, 2, QTableWidgetItem(str(descripcion)))

        self.transactionTableView.verticalHeader().hide()
        self.transactionTableView.resizeColumnsToContents()
        self.transactionTableView.setHorizontalHeaderLabels(["Fecha", "Cantidad", "Desc"])
        self.transactionTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Subscriptions
        self.subscriptionTableView = TableWidget(self)
        self.subscriptionTableView.setBorderVisible(True)
        self.subscriptionTableView.setBorderRadius(8)

        self.subscriptionTableView.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.subscriptionTableView.setWordWrap(False)
        self.subscriptionTableView.setRowCount(4)
        self.subscriptionTableView.setColumnCount(2)

        # obtiene las ultimas 4 suscripciones de la bd

        suscriptions = LocalDbConn.obtenerUltimasCuatroSuscripcionesDeUsuario()

        for i, suscription in enumerate(suscriptions):
            servicio = suscription[3]
            coste = suscription[2]
          
            # Asigna los valores a las celdas correspondientes
            self.subscriptionTableView.setItem(i, 0, QTableWidgetItem(str(servicio)))
            self.subscriptionTableView.setItem(i, 1, QTableWidgetItem(str(coste) + "€"))


        self.subscriptionTableView.verticalHeader().hide()
        self.subscriptionTableView.resizeColumnsToContents()
        self.subscriptionTableView.setHorizontalHeaderLabels(["Servicio", "Coste"])
        self.subscriptionTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        content_layout.addWidget(self.transactionTableView)
        content_layout.addWidget(self.subscriptionTableView)

        body_layout.addLayout(content_layout)

        layout.addWidget(self.bodyFrame)

        self.mainFrame.setStyleSheet("""
            #mainFrame {
                background-color: #3a6d91;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        self.headerFrame.setStyleSheet("""
            #headerFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        self.accountsFrame.setStyleSheet("""
            #accountsFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        self.bodyFrame.setStyleSheet("""
            #bodyFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        main_layout.addWidget(self.mainFrame)

    def create_account_card(self, balance, account_type, number):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #dde8f0;
                border-radius: 12px;
                padding: 15px;
                color: #333;
            }
            QLabel {
                font-size: 14px;
            }
        """)
        card_layout = QVBoxLayout(card)

        balance_label = TitleLabel(balance)
        balance_label.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align balance to the right

        account_type_label = QLabel(f"Cuenta {account_type}")
        number_label = QLabel(f"{number}")

        card_layout.addWidget(balance_label)
        card_layout.addWidget(account_type_label)
        card_layout.addWidget(number_label)

        return card
