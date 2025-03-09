import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, TitleLabel, PrimaryPushButton

import home_screen
import loans_screen
import transactions_screen
import subscriptions_screen
import settings_screen
import utils

class App(MSFluentWindow):
    def __init__(self, username):
        super().__init__()

        # Creación de las diferentes pantallas de la aplicación
        self.home_screen = home_screen.HomeScreen(username)
        self.loans_screen = loans_screen.LoansScreen()
        self.transactions_screen = transactions_screen.TransactionsScreen()
        self.subscriptions_screen = subscriptions_screen.SubscriptionsScreen()
        self.settings_screen = settings_screen.SettingsScreen()

        # Agregar las pantallas a la interfaz de navegación con iconos y nombres
        self.addSubInterface(self.home_screen, QIcon(utils.resource_path("assets/icons/home.svg")), "Home")
        self.addSubInterface(self.loans_screen, QIcon(utils.resource_path("assets/icons/accounts.svg")), "Préstamos")
        self.addSubInterface(self.transactions_screen, QIcon(utils.resource_path("assets/icons/transaction.svg")), "Pagos")
        self.addSubInterface(self.subscriptions_screen, QIcon(utils.resource_path("assets/icons/subscription.svg")), "Subs")
        self.addSubInterface(self.settings_screen, QIcon(utils.resource_path("assets/icons/settings.svg")), "Ajustes", position=NavigationItemPosition.BOTTOM)
        
        # Establecer la pantalla de inicio como la predeterminada
        self.navigationInterface.setCurrentItem(self.home_screen.objectName())
        
        # Configuración de la ventana principal
        self.resize(900, 700)
        self.setWindowTitle(f"Banco CostaSur - {username}")
        self.setWindowIcon(QIcon(utils.resource_path("assets/iconoBanco.svg")))

        # Definir el ancho mínimo de cada pantalla
        for screen in [self.home_screen, self.loans_screen, self.transactions_screen, self.subscriptions_screen, self.settings_screen]:
            screen.setMinimumWidth(600)

        # Centrar la ventana en la pantalla del usuario
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def changeEvent(self, event):
        """
        Maneja el evento de cambio de estado de la ventana.
        Si la ventana se maximiza, ajusta su tamaño a la pantalla disponible.
        """
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() == Qt.WindowState.WindowMaximized:
                self.setGeometry(QApplication.primaryScreen().availableGeometry())  
        super().changeEvent(event)
