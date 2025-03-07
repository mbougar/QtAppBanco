import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, TitleLabel, PrimaryPushButton, HyperlinkButton, LineEdit, ImageLabel, MessageBox, MessageDialog
from auth import PyrebaseAuth
from local_db_con import LocalDbConn

class LoginScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.left_image_label = ImageLabel(self)
        pixmap_left = QPixmap("assets/bancoFondo.png").scaled(
            600, 600, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation
        )
        self.left_image_label.setPixmap(pixmap_left)
        self.left_image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_image_label.setScaledContents(True)
        
        right_container = QVBoxLayout()
        right_container.setContentsMargins(20, 20, 20, 20)  # Small margin on the right
        right_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.title = TitleLabel("Iniciar Sesión")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.user_input = LineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.password_input = LineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.login_button = PrimaryPushButton("Ingresar")
        self.register_button = HyperlinkButton("", "¿No tienes cuenta? Registrate")
        
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        
        right_container.addItem(top_spacer)
        right_container.addWidget(self.title)
        right_container.addWidget(self.user_input)
        right_container.addWidget(self.password_input)
        right_container.addWidget(self.login_button)
        right_container.addWidget(self.register_button)
        right_container.addItem(bottom_spacer)
        
        main_layout.addWidget(self.left_image_label)
        main_layout.addLayout(right_container)
        
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.go_to_register)

    def login(self):
        username = self.user_input.text()
        password = self.password_input.text()


        ## Controlar que el usuario y la contraseña sean correctos con auth.sign_in_with_email_and_password
        ## Pillar la informacion desde local si es que inicia sesion


        pyrebaseAuth = PyrebaseAuth()
        #localDbConn = LocalDbConn()

        try:
            pyrebaseAuth.login(username, password)
            LocalDbConn.cargarUserInfo(username)
            self.main_window.open_banking_app(username)
        except Exception as e:
            message = MessageDialog(
                "Error",
                str(e),
                #"Usuario o contraseña incorrectos",
                self
            )
            message.exec()
    
        """
        if username in self.main_window.users and self.main_window.users[username] == password:
            self.main_window.open_banking_app(username)
        else:
            
            message = MessageDialog(
                "Error",
                "Usuario o contraseña incorrectos",
                self
            )
            message.exec()
        """

    def go_to_register(self):
        self.main_window.stacked_widget.setCurrentIndex(1)