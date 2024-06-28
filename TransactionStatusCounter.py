
import braintree
import datetime
import sys
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class TransactionWidget(QWidget):
    def __init__(self, transaction_data):
        super(TransactionWidget, self).__init__()
        self.setAutoFillBackground(True)

        # Example: Display transaction amount
        successful_transaction_count = QLabel(f"hello testing 123")

        # Example: Display customer name
        failed_transaction_count = QLabel(f"goodby testing 456")

        # Add labels to layout
        layout = QVBoxLayout()
        layout.addWidget(successful_transaction_count)
        layout.addWidget(failed_transaction_count)
        self.setLayout(layout)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        
        successful_transaction_count = {"count": "500"}
        failed_transaction_count = {"count": "50"}

        widget1 = TransactionWidget(successful_transaction_count)
        widget2 = TransactionWidget(failed_transaction_count)

        layout = QVBoxLayout()

        layout.addWidget(Color('red'))
        layout.addWidget(Color('green'))
        layout.addWidget(Color('blue'))

        layout.addWidget(widget1)
        layout.addWidget(widget2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


gateway = braintree.BraintreeGateway(
  braintree.Configuration(
      braintree.Environment.Sandbox,
      merchant_id="pzrgxphnvtycmdhq",
      public_key="932hj9f244t2bf6f",
      private_key="74a190cdf990805edd5a329d5bff37c0"
  )
)

client_token = gateway.client_token.generate({
})

print("Client token: " + client_token);

collection = gateway.transaction.search(
  braintree.TransactionSearch.created_at.between(
    datetime.datetime(2022, 10, 1),
    datetime.datetime(2022, 12, 31)
  )
)

for transaction in collection.items:
    print (transaction.amount)

