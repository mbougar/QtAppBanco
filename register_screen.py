import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import TitleLabel, PrimaryPushButton, HyperlinkButton, LineEdit, ImageLabel, MessageDialog


class RegisterScreen(QWidget):
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
        right_container.setContentsMargins(20, 20, 20, 20)
        right_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = TitleLabel("Crear Cuenta")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dni_input = LineEdit()
        self.dni_input.setPlaceholderText("DNI")

        self.name_input = LineEdit()
        self.name_input.setPlaceholderText("Nombre")

        self.surname_input = LineEdit()
        self.surname_input.setPlaceholderText("Apellido")

        self.email_input = LineEdit()
        self.email_input.setPlaceholderText("Email")

        self.phone_input = LineEdit()
        self.phone_input.setPlaceholderText("Teléfono")

        self.user_input = LineEdit()
        self.user_input.setPlaceholderText("Usuario")

        self.password_input = LineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(LineEdit.EchoMode.Password)

        self.confirm_password_input = LineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmar Contraseña")
        self.confirm_password_input.setEchoMode(LineEdit.EchoMode.Password)

        self.register_button = PrimaryPushButton("Registrarse")
        self.back_button = HyperlinkButton("", "¿Ya tienes cuenta? Inicia sesión.")

        top_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        right_container.addItem(top_spacer)
        right_container.addWidget(self.title)
        right_container.addWidget(self.dni_input)
        right_container.addWidget(self.name_input)
        right_container.addWidget(self.surname_input)
        right_container.addWidget(self.email_input)
        right_container.addWidget(self.phone_input)
        right_container.addWidget(self.user_input)
        right_container.addWidget(self.password_input)
        right_container.addWidget(self.confirm_password_input)
        right_container.addWidget(self.register_button)
        right_container.addWidget(self.back_button)
        right_container.addItem(bottom_spacer)

        main_layout.addWidget(self.left_image_label)
        main_layout.addLayout(right_container)

        self.register_button.clicked.connect(self.register)
        self.back_button.clicked.connect(self.go_back)

    def register(self):
        username = self.user_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if username in self.main_window.users:
            message = MessageDialog("Error", "El usuario ya existe", self)
            message.exec()
            return

        if password != confirm_password:
            message = MessageDialog("Error", "Las contraseñas no coinciden", self)
            message.exec()
            return

        self.main_window.users[username] = password ## Aqui metes al usuario en la base de datos

        message = MessageDialog("Éxito", "Usuario registrado con éxito", self)
        message.exec()
        self.go_back()

    def go_back(self):
        self.main_window.stacked_widget.setCurrentIndex(0)  # Volver a la pantalla de login
