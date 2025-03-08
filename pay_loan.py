import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, CaptionLabel, setTheme, Theme, ProgressRing, DoubleSpinBox 


class PayLoanMessageBox(MessageBoxBase):

    def __init__(self, parent=None, rangeMin=0.00, rangeMax=1087.20):
        super().__init__(parent)

        self.payAmount = None 

        self.titleLabel = SubtitleLabel("Pagar Préstamo", self)
        self.viewLayout.addWidget(self.titleLabel)

        self.widget.setMinimumWidth(350)

        self.rangeMax = rangeMax
        self.rangeMin = rangeMin

        self.box_layout = QHBoxLayout(self)

        # Progress Ring
        self.progressRing = ProgressRing(self)
        self.progressRing.setValue(0)
        self.progressRing.setTextVisible(True)
        self.progressRing.setFixedSize(100, 100)

        # Double Spin Box (for float values)
        self.spinBox = DoubleSpinBox(self)
        self.spinBox.setRange(self.rangeMin, self.rangeMax)
        self.spinBox.setSingleStep(self.rangeMax / 100)  # Allow increments of ~1%
        self.spinBox.setDecimals(2)  # Show 2 decimal places
        self.spinBox.setValue(0.00)  # Default value
        self.spinBox.valueChanged.connect(self.updateProgress)  # Sync values
        self.spinBox.setMinimum(0.00)

        # Add widgets to layout
        self.box_layout.addWidget(self.progressRing, 0, Qt.AlignmentFlag.AlignHCenter)
        self.box_layout.addWidget(self.spinBox, 0, Qt.AlignmentFlag.AlignHCenter)

        self.warningLabelGeneral = CaptionLabel("Datos inválidos")
        self.warningLabelGeneral.setTextColor("#cf1010", QColor(255, 28, 32))
        self.warningLabelGeneral.hide()

        self.viewLayout.addLayout(self.box_layout)
        
        # change the text of button
        self.yesButton.setText("Aceptar")
        self.cancelButton.setText("Cancelar")

    def updateProgress(self, value):
        percentage = (value / self.rangeMax) * 100  # Normalize the value
        self.payAmount = value
        self.progressRing.setValue(int(percentage))  # Convert to int for ProgressRing

    def validate(self):
        try:
            a = 1
        except Exception:
            self.warningLabelGeneral.show()
            return False
        return True
        
    def getPayAmount(self):
        return self.payAmount

