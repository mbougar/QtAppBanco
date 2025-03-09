import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import TitleLabel, PrimaryPushButton, HyperlinkButton, LineEdit, ImageLabel, MessageDialog
from auth import PyrebaseAuth
from local_db_con import LocalDbConn
from model.user_model import User

import utils

class RegisterScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Diseño principal dividido en dos secciones (izquierda: imagen, derecha: formulario)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Imagen de la izquierda
        self.left_image_label = ImageLabel(self)
        pixmap_left = QPixmap(utils.resource_path("assets/bancoFondo.png")).scaled(
            600, 600, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation
        )
        self.left_image_label.setPixmap(pixmap_left)
        self.left_image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_image_label.setScaledContents(True)

        # Contenedor de la derecha con los campos del formulario
        right_container = QVBoxLayout()
        right_container.setContentsMargins(20, 20, 20, 20)
        right_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título del formulario
        self.title = TitleLabel("Crear Cuenta")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Campos de entrada de datos
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
        self.password_input.setEchoMode(LineEdit.EchoMode.Password)  # Ocultar la contraseña

        self.confirm_password_input = LineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmar Contraseña")
        self.confirm_password_input.setEchoMode(LineEdit.EchoMode.Password)  # Ocultar la confirmación de contraseña

        # Botón de registro y enlace para volver a iniciar sesión
        self.register_button = PrimaryPushButton("Registrarse")
        self.back_button = HyperlinkButton("", "¿Ya tienes cuenta? Inicia sesión.")

        # Espaciadores para centrar el contenido
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Agregar los elementos al contenedor derecho
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

        # Agregar las secciones al diseño principal
        main_layout.addWidget(self.left_image_label)
        main_layout.addLayout(right_container)

        # Conectar botones a sus respectivas funciones
        self.register_button.clicked.connect(self.register)
        self.back_button.clicked.connect(self.go_back)

    def register(self):
        """ Función que maneja el registro del usuario """
        username = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Verificar que las contraseñas coincidan
        if password != confirm_password:
            message = MessageDialog("Error", "Las contraseñas no coinciden", self)
            message.exec()
            return

        # Verificar que la contraseña tenga al menos 6 caracteres
        if len(password) < 6:
            message = MessageDialog("Error", "La contraseña debe tener al menos 6 caracteres", self)
            message.exec()
            return

        # Verificar si el DNI ya está registrado en la base de datos local
        if LocalDbConn.comprobarDni(self.dni_input.text()):
            message = MessageDialog("Error", "El DNI ya está registrado", self)
            message.exec()
            return

        # Verificar si el correo ya está registrado en la base de datos local
        if LocalDbConn.comprobarEmail(self.email_input.text()):
            message = MessageDialog("Error", "El email ya está registrado", self)
            message.exec()
            return

        # Crear instancia de autenticación con Pyrebase
        pyrebaseAuth = PyrebaseAuth()
        userToInsert = User(
            self.dni_input.text(),
            self.name_input.text(),
            self.surname_input.text(),
            self.email_input.text(),
            self.phone_input.text()
        )

        try:
            # Registrar usuario en Pyrebase y en la base de datos local
            pyrebaseAuth.register(username, password)
            LocalDbConn.insertUser(userToInsert)
            LocalDbConn.cargarUserInfo(userToInsert.email)
        except Exception as e:
            # Si el email ya está registrado, se muestra un mensaje de error
            message = MessageDialog("Error", "El email ya ha sido registrado", self)
            message.exec()
            return

        # Mensaje de éxito y regreso a la pantalla de inicio de sesión
        message = MessageDialog("Éxito", "Usuario registrado con éxito", self)
        message.exec()
        self.go_back()

    def go_back(self):
        """ Cambia a la pantalla de inicio de sesión """
        self.main_window.stacked_widget.setCurrentIndex(0)  # Volver a la pantalla de login
