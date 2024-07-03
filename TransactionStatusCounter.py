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

        # Call handle_calendar_click function when the user clicks a date in the calendar.
        # UPDATE: Instead using the "clicked" handler here. Better allows for clicking the same date repeatedly.
        self.calendar.clicked.connect(self.handle_calendar_click) 

        transaction_counts = {
            "successful_transaction_count": {"count": 0},
            "failed_transaction_count": {"count": 0}
        }

        collection = gateway.transaction.search(
          braintree.TransactionSearch.created_at.between(
            datetime.datetime(2024, 6, 1),
            datetime.datetime(2024, 6, 5)
          )
        )

        for transaction in collection.items:
            if transaction.status in ("authorized", "submitted_for_settlement", "settling", "settled"):
                #print("Successful transaction: " + transaction.id)
                transaction_counts["successful_transaction_count"]["count"] += 1
            elif transaction.status in ("processor_declined", "gateway_rejected", "failed"):
                #print("Failed transaction: " + transaction.id)
                transaction_counts["failed_transaction_count"]["count"] += 1

        countWidget = TransactionWidget(transaction_counts)

        layout = QVBoxLayout()

        layout.addWidget(self.calendar)
        layout.addWidget(countWidget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # Changing this function up a bit.
    def handle_calendar_click(self, date):
        # The start_date and end_date variables are initially set as None.
        # So first we check if start_date has a value.
        if not self.start_date:
            # If not, set it to whatever date was clicked.
            self.start_date = date
            print(f"Start date: {self.start_date.toString('yyyy-MM-dd')}")
        else:
            # If it does, instead set the end_date to whatever date was clicked.
            self.end_date = date
            print(f"End date: {self.end_date.toString('yyyy-MM-dd')}")
        # This function allows the user to enter the same date twice, so the user can search a single date if they want.
        # TODO: Allow the start_date and end_date to be overwritten. So a new date range can be searched.


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


client_token = gateway.client_token.generate({
})
