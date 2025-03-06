import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, TitleLabel, PrimaryPushButton

import app as banking_app
import login_screen
import register_screen
import pyrebase

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banco CostaSur")
        self.setFixedSize(1000, 600)
        self.setContentsMargins


        self.users = {"admin": "1234"}  # Sacamos de la base de datos

        self.stacked_widget = QStackedWidget(self)

        self.login_screen = login_screen.LoginScreen(self)
        self.register_screen = register_screen.RegisterScreen(self)
        self.banking_app = None

        self.stacked_widget.addWidget(self.login_screen)   # Index 0 -> Login
        self.stacked_widget.addWidget(self.register_screen)  # Index 1 -> Registro

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)

    def open_banking_app(self, username):
        self.banking_app = banking_app.App(username)
        self.banking_app.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()