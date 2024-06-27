
import braintree
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPalette, QColor

# Only needed for access to command line arguments
import sys

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.

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

