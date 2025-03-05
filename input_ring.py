# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout
from qfluentwidgets import ProgressRing, DoubleSpinBox  # Use DoubleSpinBox for float values

class InputRing(QWidget):
    def __init__(self, rangeMin=0.00, rangeMax=1087.20):
        super().__init__()

        self.rangeMax = rangeMax
        self.rangeMin = rangeMin

        # Layout
        self.box_layout = QHBoxLayout(self)

        # Progress Ring
        self.progressRing = ProgressRing(self)
        self.progressRing.setValue(0)  # Default value (must be an int)
        self.progressRing.setTextVisible(True)
        self.progressRing.setFixedSize(100, 100)  # Adjust size if needed

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

        self.setLayout(self.box_layout)
        self.resize(300, 300)  # Adjust window size if needed

    def updateProgress(self, value):
        """ Convert the payment amount to percentage (0 - 100) """
        percentage = (value / self.rangeMax) * 100  # Normalize the value
        self.progressRing.setValue(int(percentage))  # Convert to int for ProgressRing

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = InputRing(0.00, 234.56)
    w.show()
    app.exec()