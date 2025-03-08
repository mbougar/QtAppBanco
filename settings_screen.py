from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import (
    PrimaryPushButton, StrongBodyLabel, Slider,
    setTheme, setThemeColor, Theme
)

class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsScreen")  # Asignamos un nombre único al widget

        # Layout principal con márgenes y espacio entre los elementos
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes para evitar que los elementos lleguen a los bordes
        layout.setSpacing(15)  # Espaciado entre los elementos dentro del layout

        # Título centrado
        self.title_label = StrongBodyLabel("⚙️ Settings", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centramos el texto
        layout.addWidget(self.title_label)  # Añadimos el título al layout principal

        # Botón para cambiar el tema
        self.theme_button = PrimaryPushButton("🌙 Cambiar acentos", self)
        self.theme_button.clicked.connect(self.toggle_theme)  # Conectamos la acción de cambio de tema
        self.theme_button.setFixedHeight(40)  # Ajustamos la altura del botón para un aspecto más consistente
        layout.addWidget(self.theme_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Centramos el botón en el layout

        # Sección para ajustar el tamaño de la fuente
        font_layout = QHBoxLayout()  # Usamos un layout horizontal para alinear el texto y el slider
        font_layout.setSpacing(10)  # Espaciado entre la etiqueta y el slider

        self.font_label = QLabel("Tamaño fuente:", self)  # Etiqueta para el tamaño de fuente
        font_layout.addWidget(self.font_label)  # Añadimos la etiqueta al layout horizontal

        # Slider para cambiar el tamaño de la fuente
        self.font_slider = Slider(Qt.Orientation.Horizontal, self)  # Slider horizontal
        self.font_slider.setRange(10, 24)  # Establecemos el rango del slider (de 10 a 24)
        self.font_slider.setValue(14)  # Valor inicial del slider
        self.font_slider.setFixedWidth(150)  # Ajustamos el ancho del slider
        self.font_slider.valueChanged.connect(self.change_font_size)  # Conectamos el cambio de valor al método
        font_layout.addWidget(self.font_slider)  # Añadimos el slider al layout horizontal

        layout.addLayout(font_layout)  # Añadimos el layout horizontal al layout principal

        # Espacio flexible para empujar los elementos hacia la parte superior
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.custom_theme = False  # Variable que controla si el tema es personalizado o no

    def toggle_theme(self):
        if self.custom_theme:  # Si el tema ya es personalizado, lo restablecemos al claro
            setTheme(Theme.LIGHT)
        else:  # Si el tema no es personalizado, aplicamos un tema claro con color personalizado
            setTheme(Theme.LIGHT)
            setThemeColor(QColor("#9575CD"))  # Establecemos un color personalizado para el tema

        self.custom_theme = not self.custom_theme  # Cambiamos el estado del tema

    def change_font_size(self, value):
        self.setStyleSheet(f"QWidget {{ font-size: {value}px; }}")  # Actualizamos el tamaño de la fuente en todo el widget
