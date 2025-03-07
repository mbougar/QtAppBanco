import sys
from PyQt6.QtCore import Qt, QDate, QSize, QEvent
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QDateEdit, QFrame
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, FluentIcon as FIF, setTheme, Theme
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QHeaderView
from qfluentwidgets import TableWidget, setTheme, Theme, FluentIconBase, StrongBodyLabel, TitleLabel, PixmapLabel, PushButton, PrimaryPushButton, MessageBox

import add_loan
import pay_loan

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
        self.loanTableView.setColumnCount(5)
        self.loanTableView.setColumnHidden(1, True)
        loans = [
            ["12000.00€", "2%", "16 meses", "1", "Pendiente"],
            ["5000.00€", "3.5%", "12 meses", "2", "Pendiente"],
            ["15000.00€", "4%", "24 meses", "3", "Pendiente"],
            ["0€", "2.8%", "18 meses", "4", "Pagado"],
            ["20000.00€", "5%", "36 meses", "5", "Pendiente"],
            ["3000.00€", "1.5%", "6 meses", "6", "Pendiente"],
            ["0€", "3%", "20 meses", "7", "Pagado"],
            ["7000.00€", "2.5%", "14 meses", "8", "Pendiente"],
            ["25000.00€", "5.2%", "48 meses", "9", "Pendiente"],
            ["0€", "1%", "3 meses", "10", "Pagado"],
            ["4500.00€", "2.3%", "10 meses", "11", "Pendiente"],
            ["18000.00€", "4.5%", "30 meses", "12", "Pendiente"],
            ["0€", "3.1%", "15 meses", "13", "Pagado"],
            ["22000.00€", "4.8%", "40 meses", "14", "Pendiente"],
            ["9500.00€", "2.7%", "22 meses", "15", "Pendiente"],
            ["13000.00€", "3.2%", "18 meses", "16", "Pendiente"],
            ["0€", "1.8%", "8 meses", "17", "Pagado"],
            ["17000.00€", "4.2%", "28 meses", "18", "Pendiente"],
            ["11000.00€", "3.6%", "20 meses", "19", "Pendiente"],
            ["0€", "2.9%", "25 meses", "20", "Pagado"],
            ["3200.00€", "1.2%", "5 meses", "21", "Pendiente"],
            ["9000.00€", "2.4%", "12 meses", "22", "Pendiente"],
            ["27000.00€", "5.5%", "50 meses", "23", "Pendiente"],
            ["0€", "3.8%", "26 meses", "24", "Pagado"],
            ["3500.00€", "1.7%", "7 meses", "25", "Pendiente"],
            ["12500.00€", "3.3%", "19 meses", "26", "Pendiente"],
            ["0€", "4.6%", "34 meses", "27", "Pagado"],
            ["7800.00€", "2.6%", "13 meses", "28", "Pendiente"],
            ["15500.00€", "3.9%", "23 meses", "29", "Pendiente"],
            ["0€", "4.4%", "32 meses", "30", "Pagado"]
        ]



        loans += loans
        for i, loanInfo in enumerate(loans):
            for j in range(5):
                item = QTableWidgetItem(loanInfo[j])
                if j == 4:  # Columna "Estado"
                    if loanInfo[j] == "Pendiente":
                        item.setBackground(QColor(255, 200, 200))  # Rojo suave
                    elif loanInfo[j] == "Pagado":
                        item.setBackground(QColor(200, 255, 200))  # Verde suave
                self.loanTableView.setItem(i, j, item)

        self.loanTableView.verticalHeader().hide()
        self.loanTableView.resizeColumnsToContents()
        self.loanTableView.setHorizontalHeaderLabels(["Monto Restante", "id", "Interes", "Plazo", "Estado"])
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
            message = MessageBox(
                "Alerta",
                "No hay ningún prestamo seleccionado.",
                self
            )
            message.yesButton.setText("Aceptar")
            message.cancelButton.setText("Cancelar")
            return

        try:
            selected_row = selected_items[0].row()
            loan_data = [
                self.loanTableView.item(selected_row, col).text() if self.loanTableView.item(selected_row, col) else "N/A"
                for col in range(self.loanTableView.columnCount())
            ]

            message = pay_loan.PayLoanMessageBox(self, 0.0, float(loan_data[0].replace("€", "")))
            if message.exec():
                loanData = message.getPayAmount()

                ## Aqui tomas los datos y actualizas el prestamo, la id del prestamo sera loan_data[1]

                print(loanData)


        except Exception as e:
            print(e)

