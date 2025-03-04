import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, CaptionLabel, setTheme, Theme


class AddLoanMessageBox(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.loanData = None 

        self.titleLabel = SubtitleLabel("Pedir Préstamo", self)
        self.loanAmount = LineEdit(self)
        self.loanInterest = LineEdit(self)
        self.loanLength = LineEdit(self)

        self.loanAmount.setPlaceholderText("Cantidad a solicitar")
        self.loanInterest.setPlaceholderText("% Interes")
        self.loanLength.setPlaceholderText("Plazo (meses)")
        self.loanAmount.setClearButtonEnabled(True)

        self.warningLabelAmount = CaptionLabel("Datos inválidos")
        self.warningLabelAmount.setTextColor("#cf1010", QColor(255, 28, 32))
        self.warningLabelInterest = CaptionLabel("Datos inválidos")
        self.warningLabelInterest.setTextColor("#cf1010", QColor(255, 28, 32))
        self.warningLabelLength = CaptionLabel("Datos inválidos")
        self.warningLabelLength.setTextColor("#cf1010", QColor(255, 28, 32))
        self.warningLabelGeneral = CaptionLabel("Datos inválidos")
        self.warningLabelGeneral.setTextColor("#cf1010", QColor(255, 28, 32))

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.loanAmount)
        self.viewLayout.addWidget(self.warningLabelAmount)
        self.viewLayout.addWidget(self.loanInterest)
        self.viewLayout.addWidget(self.warningLabelInterest)
        self.viewLayout.addWidget(self.loanLength)
        self.viewLayout.addWidget(self.warningLabelLength)
        self.viewLayout.addWidget(self.warningLabelGeneral)
        self.warningLabelAmount.hide()
        self.warningLabelInterest.hide()
        self.warningLabelLength.hide()
        self.warningLabelGeneral.hide()

        # change the text of button
        self.yesButton.setText("Aceptar")
        self.cancelButton.setText("Cancelar")

        self.widget.setMinimumWidth(350)

        # self.hideYesButton()

    def validate(self):
        try:
            amount = float(self.loanAmount.text())
            interest = float(self.loanInterest.text())
            length = int(self.loanLength.text())

            isValidAmount = True
            isValidInterest = True
            isValidLength = True

            if not (1 <= amount <= 1000000):
                isValidAmount = False
                self.warningLabelAmount.setText("La cantidad a solicitar es inválida")
                self.warningLabelAmount.setHidden(isValidAmount)
            
            if interest <= 0:  # Interest must be greater than 0
                isValidInterest = False
                self.warningLabelInterest.setText("El interés debe ser mayor a 0")
                self.warningLabelInterest.setHidden(isValidInterest)
            
            if length <= 0:  # Loan term must be greater than 0
                isValidLength = False
                self.warningLabelLength.setText("El plazo debe ser mayor a 0")
                self.warningLabelLength.setHidden(isValidLength)

            self.loanData = (amount, interest, length)

            self.loanAmount.setError(not isValidAmount)
            self.loanInterest.setError(not isValidInterest)
            self.loanLength.setError(not isValidLength)

            return (isValidAmount and isValidInterest and isValidLength)

        except ValueError:
            self.warningLabelGeneral.show()
            self.loanAmount.setError(True)
            self.loanInterest.setError(True)
            self.loanLength.setError(True)
            return False
        
    def getLoanData(self):
        return self.loanData

