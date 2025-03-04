import sys
from PyQt6.QtCore import Qt, QDate, QSize, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QDateEdit
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, FluentIcon as FIF, setTheme, Theme
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QHeaderView
from qfluentwidgets import TableWidget, setTheme, Theme, FluentIconBase, StrongBodyLabel, TitleLabel, PixmapLabel

import home_screen
import loans_screen
import transactions_screen
import subscriptions_screen
import settings_screen

class BankingApp(MSFluentWindow):
    def __init__(self):
        super().__init__()

        self.home_screen = home_screen.HomeScreen("User")
        self.loans_screen = loans_screen.LoansScreen()
        self.transactions_screen = transactions_screen.TransactionsScreen()
        self.subscriptions_screen = subscriptions_screen.SubscriptionsScreen()
        self.settings_screen = settings_screen.SettingsScreen()

        self.addSubInterface(self.home_screen, QIcon("assets/icons/home.svg"), "Home")
        self.addSubInterface(self.loans_screen, QIcon("assets/icons/accounts.svg"), "Préstamos")
        self.addSubInterface(self.transactions_screen, QIcon("assets/icons/transaction.svg"), "Transacciones")
        self.addSubInterface(self.subscriptions_screen, QIcon("assets/icons/subscription.svg"), "Subscripciones")
        self.addSubInterface(self.settings_screen, QIcon("assets/icons/settings.svg"), "Ajustes", position=NavigationItemPosition.BOTTOM)

        self.navigationInterface.setCurrentItem(self.home_screen.objectName())
        self.resize(900, 700)
        self.setWindowTitle("Banco CostaSur")
        self.setWindowIcon(QIcon("assets/iconoBanco.svg"))      

        ## Establecemos un ancho mínimo en las subpantallas dentro de la pantalla fluida
        for screen in [self.home_screen, self.loans_screen, self.transactions_screen, self.subscriptions_screen, self.settings_screen]:
            screen.setMinimumWidth(600)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() == Qt.WindowState.WindowMaximized:
                self.setGeometry(QApplication.primaryScreen().availableGeometry())  # Ajustar a la pantalla disponible
        super().changeEvent(event)



if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    window = BankingApp()
    window.show()
    app.exec()
