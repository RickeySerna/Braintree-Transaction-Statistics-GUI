import braintree
import datetime
import sys
import argparse
from datetime import date, datetime, timedelta
from PyQt6.QtCore import QDate, Qt
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

class DateWidget(QWidget):
    def __init__(self, start_date, end_date):
        super(DateWidget, self).__init__()

        formatted_start_date = start_date.strftime("%-m/%-d/%Y")
        formatted_end_date = end_date.strftime("%-m/%-d/%Y")
        
        self.search_range = QLabel(f"Search range: {formatted_start_date} - {formatted_end_date}")
        self.search_range.setStyleSheet("text-decoration: underline; color: red;")
        self.search_range.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.search_range)
        self.setLayout(layout)

    def update_date_range(self, start_date, end_date):
        
        print(f"Start date inside update_date_range: {start_date}")
        print(f"End date inside update_date_range: {end_date}")

        start_python_date = date(start_date.year(), start_date.month(), start_date.day())
        end_python_date = date(end_date.year(), end_date.month(), end_date.day())

        formatted_start_date = start_python_date.strftime("%-m/%-d/%Y")
        formatted_end_date = end_python_date.strftime("%-m/%-d/%Y")

        print(f"Formatted start date: {formatted_start_date}")
        print(f"Formatted end date: {formatted_end_date}")

        self.search_range.setText(f"Search range: {formatted_start_date} - {formatted_end_date}")

class MainWindow(QMainWindow):

    def __init__(self, start_date=None, end_date=None):
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
        self.start_date = start_date
        self.end_date = end_date

        print(f"self.start_date in MainWindow: {self.start_date}")
        print(f"self.end_date in MainWindow: {self.end_date}")

        if (self.start_date == None) and (self.end_date == None):
            print(f"Do the default search")

            # Calculating todays date and the date 30 days before todays date.
            # This will be immediately passed into a transaction.search() when the file is run.
            # This is so that the user can immediately see the stats for their transactions in the last 30 days.
            # If they want to search a new date range, they're free to do so with the calendar, but the
            ## last 30 days' data is immediately and quickly supplied.

            # Tack on an extra day when calculating todays date because this method cuts the date time off at 00:00:00.
            # So adding an extra day effectively makes it search the whole of todays date through midnight. (date = tomorrow at 00:00:... aka midnight of today)
            todayDate = date.today()
            # Format todays date into the format accepted by the transaction.search() call.
            todayDateFormatted = datetime(todayDate.year, todayDate.month, todayDate.day, 23, 59, 59)

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

            self.datesWidget = DateWidget(thirtyDaysAgoFormatted, todayDateFormatted)
            self.countWidget = TransactionWidget(transaction_counts)
            
        else:
            print(f"Use the arguments provided")

        # Call handle_calendar_click function when the user clicks a date in the calendar.
        # UPDATE: Instead using the "clicked" handler here. Better allows for clicking the same date repeatedly.
        self.calendar.clicked.connect(self.handle_calendar_click)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.datesWidget)
        self.layout.addWidget(self.countWidget)

        widget = QWidget()
        widget.setLayout(self.layout)
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

            self.datesWidget.update_date_range(self.start_date, self.end_date)
            
            self.new_transaction_search(self.start_date, self.end_date)

            self.start_date = None
            self.end_date = None
        # This function allows the user to enter the same date twice, so the user can search a single date if they want.
        # TODO: Allow the start_date and end_date to be overwritten. So a new date range can be searched.

    def new_transaction_search(self, startDate, endDate):

        startDateFormatted = datetime(startDate.year(), startDate.month(), startDate.day())
        endDateFormatted = datetime(endDate.year(), endDate.month(), endDate.day(), 23, 59, 59)

        print(f"New start date: {startDateFormatted}")
        print(f"New end date: {endDateFormatted}")

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

        self.update_widget_data(new_transaction_counts)


    def update_widget_data(self, new_data):
        if hasattr(self, 'countWidget'):
            self.layout.removeWidget(self.countWidget)
            self.countWidget.deleteLater()

        self.countWidget = TransactionWidget(new_data)
        self.layout.addWidget(self.countWidget)


def main():

    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser(description="Transaction search")
    parser.add_argument("start_date", nargs="?", default=None, help="Start date (format: MM/DD/YYYY)")
    parser.add_argument("end_date", nargs="?", default=None, help="End date (format: MM/DD/YYYY)")
    args = parser.parse_args()

    if args.start_date and args.end_date:
        print(f"Start date: {args.start_date}")
        print(f"End date: {args.end_date}")
    else:
        print("Using default behavior (search within the last 30 days)")


    window = MainWindow(args.start_date, args.end_date)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
