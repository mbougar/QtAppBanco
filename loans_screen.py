import sys
from PyQt6.QtCore import Qt, QDate, QSize, QEvent
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QDateEdit, QFrame
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, FluentIcon as FIF, setTheme, Theme
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QHeaderView
from qfluentwidgets import TableWidget, setTheme, Theme, FluentIconBase, StrongBodyLabel, TitleLabel, PixmapLabel, PushButton, PrimaryPushButton

import add_loan

class LoansScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("loansScreen")
        
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
        title_layout.addWidget(TitleLabel("Préstamos"))
        layout.addWidget(self.titleFrame)

        # Loans Frame

        self.loansFrame = QFrame(self.mainFrame)
        self.loansFrame.setObjectName("loansFrame")
        loans_layout = QVBoxLayout(self.loansFrame)

        self.loanTableView = TableWidget(self)
        self.loanTableView.setBorderVisible(True)
        self.loanTableView.setBorderRadius(8)
        
        self.loanTableView.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.loanTableView.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.loanTableView.setWordWrap(False)
        self.loanTableView.setRowCount(30)
        self.loanTableView.setColumnCount(4)
        loans = [
            ["12000.00€", "2%", "16 meses", "Pendiente"],
            ["5000.00€", "3.5%", "12 meses", "Pendiente"],
            ["15000.00€", "4%", "24 meses", "Pendiente"],
            ["0€", "2.8%", "18 meses", "Pagado"],
            ["20000.00€", "5%", "36 meses", "Pendiente"],
            ["3000.00€", "1.5%", "6 meses", "Pendiente"],
            ["0€", "3%", "20 meses", "Pagado"],
            ["7000.00€", "2.5%", "14 meses", "Pendiente"],
            ["25000.00€", "5.2%", "48 meses", "Pendiente"],
            ["0€", "1%", "3 meses", "Pagado"],
            ["4500.00€", "2.3%", "10 meses", "Pendiente"],
            ["18000.00€", "4.5%", "30 meses", "Pendiente"],
            ["0€", "3.1%", "15 meses", "Pagado"],
            ["22000.00€", "4.8%", "40 meses", "Pendiente"],
            ["9500.00€", "2.7%", "22 meses", "Pendiente"],
            ["13000.00€", "3.2%", "18 meses", "Pendiente"],
            ["0€", "1.8%", "8 meses", "Pagado"],
            ["17000.00€", "4.2%", "28 meses", "Pendiente"],
            ["11000.00€", "3.6%", "20 meses", "Pendiente"],
            ["0€", "2.9%", "25 meses", "Pagado"],
            ["3200.00€", "1.2%", "5 meses", "Pendiente"],
            ["9000.00€", "2.4%", "12 meses", "Pendiente"],
            ["27000.00€", "5.5%", "50 meses", "Pendiente"],
            ["0€", "3.8%", "26 meses", "Pagado"],
            ["3500.00€", "1.7%", "7 meses", "Pendiente"],
            ["12500.00€", "3.3%", "19 meses", "Pendiente"],
            ["0€", "4.6%", "34 meses", "Pagado"],
            ["7800.00€", "2.6%", "13 meses", "Pendiente"],
            ["15500.00€", "3.9%", "23 meses", "Pendiente"],
            ["0€", "4.4%", "32 meses", "Pagado"]
        ]

        loans += loans
        for i, loanInfo in enumerate(loans):
            for j in range(4):
                item = QTableWidgetItem(loanInfo[j])
                if j == 3:  # Columna "Estado"
                    if loanInfo[j] == "Pendiente":
                        item.setBackground(QColor(255, 200, 200))  # Rojo suave
                    elif loanInfo[j] == "Pagado":
                        item.setBackground(QColor(200, 255, 200))  # Verde suave
                self.loanTableView.setItem(i, j, item)

        self.loanTableView.verticalHeader().hide()
        self.loanTableView.resizeColumnsToContents()
        self.loanTableView.setHorizontalHeaderLabels(["Monto Restante", "Interes", "Plazo", "Estado"])
        self.loanTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)        

        loans_layout.addWidget(self.loanTableView)
        layout.addWidget(self.loansFrame)

        ## Loans button frame
        self.loansButtonFrame = QFrame(self.mainFrame)
        self.loansButtonFrame.setObjectName("loansButtonFrame")
        loans_button_layout = QHBoxLayout(self.loansButtonFrame)

        self.add_loan_button = PrimaryPushButton("Pedir Préstamo")
        self.pay_loan_button = PrimaryPushButton("Pagar Préstamo")
        loans_button_layout.addWidget(self.add_loan_button)
        loans_button_layout.addWidget(self.pay_loan_button)
        layout.addWidget(self.loansButtonFrame)

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

        self.loansFrame.setStyleSheet("""
            #loansFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        self.loansButtonFrame.setStyleSheet("""
            #loansButtonFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        main_layout.addWidget(self.mainFrame)
        self.add_loan_button.clicked.connect(self.add_loan)
        self.pay_loan_button.clicked.connect(self.pay_loan)

    def add_loan(self):
        message = add_loan.AddLoanMessageBox(self)
        if message.exec():
            loanData = message.getLoanData()

            amount, interest, length = loanData

            ## Aqui tomas los datos y creas un prestamo

            print(loanData)

    def pay_loan(self):
        selected_items = self.loanTableView.selectedItems()
        if not selected_items:
            print("No loan selected.")
            return

        selected_row = selected_items[0].row()
        loan_data = [self.loanTableView.item(selected_row, col).text() for col in range(self.loanTableView.columnCount())]
        
        print(f"Selected Loan: {loan_data}")
