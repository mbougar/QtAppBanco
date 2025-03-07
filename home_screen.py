import sys
from PyQt6.QtCore import Qt, QDate, QSize, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QDateEdit, QFrame
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, FluentIcon as FIF, setTheme, Theme
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QHeaderView
from qfluentwidgets import TableWidget, setTheme, Theme, FluentIconBase, StrongBodyLabel, TitleLabel

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
        self.welcome_label = TitleLabel(f"Hola {username}, ¡Bienvenido de nuevo!")
        header_layout = QHBoxLayout(self.headerFrame)
        layout.addWidget(self.headerFrame)

        self.welcome_label = TitleLabel(f"Hola {username}, ¡Bienvenido de nuevo!")
        header_layout.addWidget(self.welcome_label)
        layout.addWidget(self.headerFrame)

        # Cuentas (Maximo 3)

        self.accountsFrame = QFrame(self.mainFrame)
        self.accountsFrame.setObjectName("accountsFrame")

        accounts_layout = QHBoxLayout(self.accountsFrame)

        ## obtener las ultimas cuentas del usuario

        accounts = [
            {"balance": "10,500€", "type": "Ahorros", "number": "1234 5678 9012 3456"},
            {"balance": "3,200€", "type": "Corriente", "number": "9876 5432 1098 7654"},
            {"balance": "22,850€", "type": "Inversión", "number": "4567 8901 2345 6789"},
            {"balance": "22,850€", "type": "Inversión", "number": "4567 8901 2345 6789"},
            {"balance": "22,850€", "type": "Inversión", "number": "4567 8901 2345 6789"},
        ]

        ## Pon la llamada a las cuentas aqui, y crea una tarjeta por cada cuenta

        for account in accounts:
            card = self.create_account_card(account["balance"], account["type"], account["number"])
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

        # get ultimas 4 suscripciones from database

        transactions = [
            ["12/3/2025", "1234.00€", "Compra Online"],
            ["12/3/2025", "11234.00€", "Compra Online"],
            ["10/3/2025", "123.00€", "Compra Online"],
            ["10/3/2025", "94.00€", "Compra Online"]
        ]
        transactions += transactions
        for i, songInfo in enumerate(transactions):
            for j in range(3):
                self.transactionTableView.setItem(i, j, QTableWidgetItem(songInfo[j]))

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

        # get ultimas 4 transactions from database


        transactions = [
            ["Netflix", "12.00€"],
            ["Amazon Prime", "11.99€"],
            ["CarsFacts", "3.00€"],
            ["Uber", "8.00€"]
        ]
        transactions += transactions
        for i, songInfo in enumerate(transactions):
            for j in range(2):
                self.subscriptionTableView.setItem(i, j, QTableWidgetItem(songInfo[j]))

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
