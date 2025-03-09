import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, CaptionLabel, setTheme, Theme, ProgressRing, DoubleSpinBox 

class PayLoanMessageBox(MessageBoxBase):

    def __init__(self, parent=None, rangeMin=0.00, rangeMax=1087.20):
        super().__init__(parent)

        self.payAmount = None  # Variable para almacenar la cantidad a pagar

        # Título del cuadro de diálogo
        self.titleLabel = SubtitleLabel("Pagar Préstamo", self)
        self.viewLayout.addWidget(self.titleLabel)

        self.widget.setMinimumWidth(350)  # Establece el ancho mínimo del cuadro de diálogo

        # Definir los valores mínimo y máximo para el pago
        self.rangeMax = rangeMax
        self.rangeMin = rangeMin

        self.box_layout = QHBoxLayout(self)  # Layout horizontal para los elementos

        # Anillo de progreso (muestra visualmente el porcentaje de pago)
        self.progressRing = ProgressRing(self)
        self.progressRing.setValue(0)  # Inicializa en 0%
        self.progressRing.setTextVisible(True)  # Muestra el porcentaje como texto
        self.progressRing.setFixedSize(100, 100)  # Tamaño fijo para el anillo

        # Caja de entrada numérica de doble precisión para el monto a pagar
        self.spinBox = DoubleSpinBox(self)
        self.spinBox.setRange(self.rangeMin, self.rangeMax)  # Establece los límites
        self.spinBox.setSingleStep(self.rangeMax / 100)  # Incrementos del 1%
        self.spinBox.setDecimals(2)  # Mostrar 2 decimales
        self.spinBox.setValue(0.00)  # Valor por defecto
        self.spinBox.valueChanged.connect(self.updateProgress)  # Sincronizar con el anillo de progreso
        self.spinBox.setMinimum(0.00)

        # Agregar widgets al layout
        self.box_layout.addWidget(self.progressRing, 0, Qt.AlignmentFlag.AlignHCenter)
        self.box_layout.addWidget(self.spinBox, 0, Qt.AlignmentFlag.AlignHCenter)

        # Etiqueta de advertencia para datos inválidos
        self.warningLabelGeneral = CaptionLabel("Datos inválidos")
        self.warningLabelGeneral.setTextColor("#cf1010", QColor(255, 28, 32))
        self.warningLabelGeneral.hide()  # Se oculta inicialmente

        self.viewLayout.addLayout(self.box_layout)  # Agrega el layout al cuadro de diálogo
        
        # Cambia el texto de los botones
        self.yesButton.setText("Aceptar")
        self.cancelButton.setText("Cancelar")

    # Método para actualizar el anillo de progreso al cambiar el valor del monto a pagar
    def updateProgress(self, value):
        percentage = (value / self.rangeMax) * 100  # Calcula el porcentaje
        self.payAmount = value  # Guarda el valor actual del monto
        self.progressRing.setValue(int(percentage))  # Actualiza el anillo de progreso

    # Método de validación (actualmente no implementado correctamente)
    def validate(self):
        try:
            a = 1  # No realiza validaciones reales, se puede mejorar
        except Exception:
            self.warningLabelGeneral.show()
            return False
        return True
       
    # Método para obtener el monto ingresado por el usuario
    def getPayAmount(self):
        return self.payAmount
