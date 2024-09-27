from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QDialog,
    QDialogButtonBox
)

class ErrorMessageBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Date Selection Error")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.message = QLabel("The end date cannot be before the start date.")
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def update_box_message(self, new_message):
        self.message.setText(f"{new_message}")

    def update_box_title(self, new_title):
        self.setWindowTitle(f"{new_title}")
