import sys
from PyQt6.QtCore import Qt, QDate, QSize, QEvent
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QDateEdit, QFrame
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, FluentIcon as FIF, setTheme, Theme
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QHeaderView
from qfluentwidgets import TableWidget, setTheme, Theme, FluentIconBase, StrongBodyLabel, TitleLabel, PixmapLabel, PushButton, PrimaryPushButton, MessageBox

import add_loan
import pay_loan
from local_db_con import LocalDbConn
from model.prestamo_model import Prestamo
from datetime import datetime

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
        self.loanTableView.setColumnCount(4)
        self.loanTableView.setColumnHidden(1, True)
        
        
        self.populate_loans()

        self.loanTableView.verticalHeader().hide()
        self.loanTableView.resizeColumnsToContents()
        self.loanTableView.setHorizontalHeaderLabels(["Monto Restante", "id", "Interes", "Plazo"])
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

    # Metodo para actualizar la tabla visual de prestamos
    def populate_loans(self):
        
        loans = LocalDbConn.obtenerTodosLosPrestamosDeUsuario()

        self.loanTableView.setRowCount(len(loans))

        for i, loanInfo in enumerate(loans):
            monto = float(loanInfo[2])
            monto = round(monto, 2)
            interes = loanInfo[3]
            plazo = loanInfo[4]

            # Asigna los valores a las celdas correspondientes
            self.loanTableView.setItem(i, 1, QTableWidgetItem(str(loanInfo[0])))
            self.loanTableView.setItem(i, 0, QTableWidgetItem(str(monto) + "€"))
            self.loanTableView.setItem(i, 2, QTableWidgetItem(str(interes) + "%"))
            self.loanTableView.setItem(i, 3, QTableWidgetItem(str(plazo) + " meses"))

    def add_loan(self):
        message = add_loan.AddLoanMessageBox(self)
        if message.exec():
            loanData = message.getLoanData()

            amount, interest, length = loanData

            ## Aqui tomas los datos y creas un prestamo
            LocalDbConn.insertarPrestamo(Prestamo(LocalDbConn.actualUser.dni, amount, interest, length, "Pending", datetime.now().strftime("%Y-%m-%d")))

            print(loanData)

            self.populate_loans()

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
            message.exec()
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
                
                print(loanData)
                print(loan_data)

                ## Aqui tomas los datos y actualizas el prestamo, la id del prestamo sera loan_data[1]
                original_loan = float(loan_data[0].replace("€","")) 
                loan_to_pay = float(message.getPayAmount())

                #Comprueba el monto a pagar, dependiendo del resultado actualiza o elimina el prestamo
                if (original_loan > loan_to_pay):
                    new_loan = original_loan - loan_to_pay
                    LocalDbConn.pagarPrestamo(new_loan, loan_data[1])
                else:
                    LocalDbConn.borrarPrestamo(loan_data[1])
        
                self.populate_loans() 
            
                print(loanData)


        except Exception as e:
            print(e)

