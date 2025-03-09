import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, CaptionLabel, setTheme, Theme
from local_db_con import LocalDbConn
from model.prestamo_model import Prestamo
from datetime import datetime

class AddLoanMessageBox(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.loanData = None  # Variable para almacenar los datos del préstamo si la validación es exitosa

        # Título del cuadro de diálogo
        self.titleLabel = SubtitleLabel("Pedir Préstamo", self)
        
        # Campos de entrada para la cantidad, interés y plazo del préstamo
        self.loanAmount = LineEdit(self)
        self.loanInterest = LineEdit(self)
        self.loanLength = LineEdit(self)

        # Texto de marcador de posición para guiar al usuario
        self.loanAmount.setPlaceholderText("Cantidad a solicitar")
        self.loanInterest.setPlaceholderText("% Interés")
        self.loanLength.setPlaceholderText("Plazo (meses)")
        self.loanAmount.setClearButtonEnabled(True)  # Habilita el botón de limpieza del campo

        # Etiquetas de advertencia para validación de datos
        self.warningLabelAmount = CaptionLabel("Datos inválidos")
        self.warningLabelAmount.setTextColor("#cf1010", QColor(255, 28, 32))
        self.warningLabelInterest = CaptionLabel("Datos inválidos")
        self.warningLabelInterest.setTextColor("#cf1010", QColor(255, 28, 32))
        self.warningLabelLength = CaptionLabel("Datos inválidos")
        self.warningLabelLength.setTextColor("#cf1010", QColor(255, 28, 32))
        self.warningLabelGeneral = CaptionLabel("Datos inválidos")
        self.warningLabelGeneral.setTextColor("#cf1010", QColor(255, 28, 32))

        # Agregar los widgets al diseño del cuadro de diálogo
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.loanAmount)
        self.viewLayout.addWidget(self.warningLabelAmount)
        self.viewLayout.addWidget(self.loanInterest)
        self.viewLayout.addWidget(self.warningLabelInterest)
        self.viewLayout.addWidget(self.loanLength)
        self.viewLayout.addWidget(self.warningLabelLength)
        self.viewLayout.addWidget(self.warningLabelGeneral)

        # Ocultar las etiquetas de advertencia al inicio
        self.warningLabelAmount.hide()
        self.warningLabelInterest.hide()
        self.warningLabelLength.hide()
        self.warningLabelGeneral.hide()

        # Personalizar los botones de la ventana emergente
        self.yesButton.setText("Aceptar")
        self.cancelButton.setText("Cancelar")

        # Establecer tamaño mínimo de la ventana emergente
        self.widget.setMinimumWidth(350)

    def validate(self):
        """
        Valida los datos ingresados en los campos de texto.
        Retorna True si todos los datos son válidos, de lo contrario, retorna False.
        """
        try:
            # Intenta convertir los valores ingresados a los tipos de datos correctos
            amount = float(self.loanAmount.text())
            interest = float(self.loanInterest.text())
            length = int(self.loanLength.text())

            isValidAmount = True
            isValidInterest = True
            isValidLength = True

            # Validación de la cantidad del préstamo (debe estar en un rango razonable)
            if not (1 <= amount <= 1000000):
                isValidAmount = False
                self.warningLabelAmount.setText("La cantidad a solicitar es inválida")
                self.warningLabelAmount.setHidden(isValidAmount)
            
            # Validación del interés (debe ser mayor a 0)
            if interest <= 0:
                isValidInterest = False
                self.warningLabelInterest.setText("El interés debe ser mayor a 0")
                self.warningLabelInterest.setHidden(isValidInterest)

            # Validación del plazo (debe ser mayor a 0 meses)
            if length <= 0:
                isValidLength = False
                self.warningLabelLength.setText("El plazo debe ser mayor a 0")
                self.warningLabelLength.setHidden(isValidLength)

            # Guardar los datos si son válidos
            self.loanData = (amount, interest, length)

            # Mostrar errores en los campos correspondientes
            self.loanAmount.setError(not isValidAmount)
            self.loanInterest.setError(not isValidInterest)
            self.loanLength.setError(not isValidLength)

            return (isValidAmount and isValidInterest and isValidLength)

        except ValueError:
            # Manejo de error en caso de que el usuario ingrese datos no numéricos
            self.warningLabelGeneral.show()
            self.loanAmount.setError(True)
            self.loanInterest.setError(True)
            self.loanLength.setError(True)
            return False
        
    def getLoanData(self):
        """
        Retorna los datos del préstamo si han sido validados correctamente.
        """
        return self.loanData

