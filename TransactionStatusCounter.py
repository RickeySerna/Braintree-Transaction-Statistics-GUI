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

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
      braintree.Environment.Sandbox,
      merchant_id="pzrgxphnvtycmdhq",
      public_key="932hj9f244t2bf6f",
      private_key="74a190cdf990805edd5a329d5bff37c0"
  )
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
        
        successful_count = transaction_data["successful_transaction_count"]["count"]
        failed_count = transaction_data["failed_transaction_count"]["count"]

        successful_transaction_count = QLabel(f"Successful transactions: {successful_count}")
        failed_transaction_count = QLabel(f"Failed transactions: {failed_count}")

        layout = QVBoxLayout()
        layout.addWidget(successful_transaction_count)
        layout.addWidget(failed_transaction_count)
        self.setLayout(layout)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        transaction_counts = {
            "successful_transaction_count": {"count": 0},
            "failed_transaction_count": {"count": 0}
        }

        collection = gateway.transaction.search(
          braintree.TransactionSearch.created_at.between(
            datetime.datetime(2024, 6, 1),
            datetime.datetime(2024, 6, 30)
          )
        )

        for transaction in collection.items:
            if transaction.status in ("authorized", "submitted_for_settlement", "settling", "settled"):
                print("Successful transaction: " + transaction.id)
                transaction_counts["successful_transaction_count"]["count"] += 1
            elif transaction.status in ("processor_declined", "gateway_rejected", "failed"):
                print("Failed transaction: " + transaction.id)
                transaction_counts["failed_transaction_count"]["count"] += 1

        widget1 = TransactionWidget(transaction_counts)

        layout = QVBoxLayout()

        layout.addWidget(Color('red'))
        layout.addWidget(Color('green'))
        layout.addWidget(Color('blue'))

        layout.addWidget(widget1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


client_token = gateway.client_token.generate({
})

print("Client token: " + client_token);
