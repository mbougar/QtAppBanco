import sys, ctypes
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, TitleLabel, PrimaryPushButton

import app as banking_app
import login_screen
import register_screen
import pyrebase
import utils

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banco CostaSur")  # Establece el título de la ventana
        self.setFixedSize(1000, 600)  # Fija el tamaño de la ventana a 1000x600 píxeles

        # Widget de pila para cambiar entre pantallas de inicio de sesión y registro
        self.stacked_widget = QStackedWidget(self)

        # Instancia de la pantalla de inicio de sesión y registro
        self.login_screen = login_screen.LoginScreen(self)
        self.register_screen = register_screen.RegisterScreen(self)
        self.banking_app = None  # Inicialmente, la aplicación bancaria no está cargada

        # Agrega las pantallas al QStackedWidget
        self.stacked_widget.addWidget(self.login_screen)   # Index 0 -> Login
        self.stacked_widget.addWidget(self.register_screen)  # Index 1 -> Registro

        # Diseño principal de la ventana
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def open_banking_app(self, username):
        """
        Método para abrir la aplicación bancaria después de iniciar sesión.
        Carga la aplicación bancaria y cierra la ventana de inicio de sesión.
        """
        self.banking_app = banking_app.App(username)  # Crea una instancia de la aplicación bancaria
        self.banking_app.show()  # Muestra la aplicación bancaria
        self.close()  # Cierra la ventana actual

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Inicializa la aplicación PyQt
    
    # Establece un identificador de la aplicación en Windows para que use el ícono correcto en la barra de tareas
    myappid = 'banco.myapp.costasur'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    # Configura el ícono de la aplicación
    app.setWindowIcon(QtGui.QIcon(utils.resource_path("iconoBanco.ico")))
    
    # Crea e inicia la ventana principal
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())  # Ejecuta el loop de eventos de la aplicación
