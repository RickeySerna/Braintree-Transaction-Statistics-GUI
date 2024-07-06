import braintree
import datetime
import sys
from datetime import date, datetime, timedelta
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

        self.gateway = braintree.BraintreeGateway(
          braintree.Configuration(
              braintree.Environment.Sandbox,
              merchant_id="pzrgxphnvtycmdhq",
              public_key="932hj9f244t2bf6f",
              private_key="74a190cdf990805edd5a329d5bff37c0"
          )
        )

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

        # Calculating todays date and the date 30 days before todays date.
        # This will be immediately passed into a transaction.search() when the file is run.
        # This is so that the user can immediately see the stats for their transactions in the last 30 days.
        # If they want to search a new date range, they're free to do so with the calendar, but the
        ## last 30 days' data is immediately and quickly supplied.

        # Tack on an extra day when calculating todays date because this method cuts the date time off at 00:00:00.
        # So adding an extra day effectively makes it search the whole of todays date through midnight. (date = tomorrow at 00:00:... aka midnight of today)
        todayDate = date.today() + timedelta(days=1)
        # Format todays date into the format accepted by the transaction.search() call.
        todayDateFormatted = datetime(todayDate.year, todayDate.month, todayDate.day)

        # Do the exact same thing to get 30 days ago's date, except take away 30 days instead of add 1.
        thirtyDaysAgo = date.today() - timedelta(days=30)
        thirtyDaysAgoFormatted = datetime(thirtyDaysAgo.year, thirtyDaysAgo.month, thirtyDaysAgo.day)

        # Run the transaction.search() call with the dates we just created and store the results into an object.
        initialCollection = self.gateway.transaction.search(
          braintree.TransactionSearch.created_at.between(
            thirtyDaysAgoFormatted,
            todayDateFormatted
          )
        )

        # Initialize the dictionary we use to count the stats on the transactions.
        transaction_counts = {
            "successful_transaction_count": {"count": 0},
            "failed_transaction_count": {"count": 0}
        }

        # Go through the transactions we pulled in the search.
        for transaction in initialCollection.items:
            # If the transaction  has a successful status, add to the success count in the dictionary.
            if transaction.status in ("authorized", "submitted_for_settlement", "settling", "settled"):
                transaction_counts["successful_transaction_count"]["count"] += 1
            # If the transaction  has a failed status, add to the fail count in the dictionary.
            elif transaction.status in ("processor_declined", "gateway_rejected", "failed"):
                transaction_counts["failed_transaction_count"]["count"] += 1

        # TODO: If the user enters a new search range, destroy these widget created with these stats^ and create a new one.

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
            self.start_date = date#datetime(date.year, date.month, date.day)
            print(f"Start date: {self.start_date}")
        else:
            # If it does, instead set the end_date to whatever date was clicked.
            self.end_date = date#datetime(date.year, date.month, date.day)
            print(f"End date: {self.end_date}")
            
            self.new_transaction_search(self.start_date, self.end_date)
        # This function allows the user to enter the same date twice, so the user can search a single date if they want.
        # TODO: Allow the start_date and end_date to be overwritten. So a new date range can be searched.

    def new_transaction_search(self, startDate, endDate):

        startDateFormatted = datetime(startDate.year(), startDate.month(), startDate.day())
        endDateFormatted = datetime(endDate.year(), endDate.month(), endDate.day())

        new_transaction_counts = {
            "successful_transaction_count": {"count": 0},
            "failed_transaction_count": {"count": 0}
        }

        newCollection = self.gateway.transaction.search(
          braintree.TransactionSearch.created_at.between(
            startDateFormatted,
            endDateFormatted
          )
        )

        for transaction in newCollection.items:
            # If the transaction  has a successful status, add to the success count in the dictionary.
            if transaction.status in ("authorized", "submitted_for_settlement", "settling", "settled"):
                print("Success transaction ID: " + transaction.id)
                new_transaction_counts["successful_transaction_count"]["count"] += 1
            # If the transaction  has a failed status, add to the fail count in the dictionary.
            elif transaction.status in ("processor_declined", "gateway_rejected", "failed"):
                print("Failed transaction ID: " + transaction.id)
                new_transaction_counts["failed_transaction_count"]["count"] += 1

        print(new_transaction_counts)

        update_widget_data(new_transaction_counts)


    def update_widget_data(self, new_data):
        # Remove the existing widget (if it exists)
        if hasattr(self, 'countWidget'):
            self.countWidget.deleteLater()  # Remove the widget from the layout

        # Create a new widget with the updated data
        self.newCountWidget = TransactionWidget(new_data)
        self.layout.addWidget(self.newCountWidget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
