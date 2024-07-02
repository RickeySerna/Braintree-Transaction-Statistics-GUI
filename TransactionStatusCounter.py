import braintree
import datetime
import sys
from PyQt6.QtCore import QDate
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
    QLineEdit,
    QCalendarWidget
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

        # Creating a calendar widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setMinimumDate(QDate(2000, 1, 1))
        self.calendar.setMaximumDate(QDate(2099, 12, 31))

        # Creating start date and end date variables which will be plugged into the Transaction.search() call.
        self.start_date = None
        self.end_date = None

        # Call handle_date_selection function when the user clicks a date in the calendar.
        self.calendar.selectionChanged.connect(self.handle_date_selection)

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

        countWidget = TransactionWidget(transaction_counts)

        layout = QVBoxLayout()

        layout.addWidget(self.calendar)
        layout.addWidget(countWidget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # This function sets the date range to be searched.
    def handle_date_selection(self):
        # First grab the date the user clicked.
        selected_date = self.calendar.selectedDate()

        # Check if start_date is currently empty.
        if self.start_date is None:
            # If it is, set it as the selected date.
            self.start_date = selected_date
            print(f"Start date: {self.start_date.toString('yyyy-MM-dd')}")
        else:
            # If it's not, instead set end_date as the selected date.
            self.end_date = selected_date
            print(f"End date: {self.end_date.toString('yyyy-MM-dd')}")
            # Reset start_date back to None in case a new search is started.
            self.start_date = None


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


client_token = gateway.client_token.generate({
})
