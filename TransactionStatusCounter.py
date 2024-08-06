import braintree
import datetime
import sys
import argparse
import math
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

class TransactionWidget(QWidget):
    def __init__(self, transaction_data):
        super(TransactionWidget, self).__init__()
        self.setAutoFillBackground(True)

        self.successful_transaction_count = transaction_data["successful_transaction_count"]["count"]
        self.transacted_amount_count = transaction_data["transacted_amount"]["count"]
        self.failed_transaction_count = transaction_data["failed_transaction_count"]["count"]
        self.declined_count = transaction_data["declined_count"]["count"]
        self.rejected_count = transaction_data["rejected_count"]["count"]
        self.failed_count = transaction_data["failed_count"]["count"]
        self.refunded_count = transaction_data["refunded_count"]["count"]
        self.total_refunded = transaction_data["total_refunded"]["count"]
        self.average_transaction_amount = transaction_data["average_transaction_amount"]["count"]
        self.credit_card_txns = transaction_data["credit_card_txns"]["count"]
        self.apple_pay_txns = transaction_data["apple_pay_txns"]["count"]
        self.google_pay_txns = transaction_data["google_pay_txns"]["count"]
        self.paypal_txns = transaction_data["paypal_txns"]["count"]

        self.successful_transaction_count_label = QLabel(f"Successful transactions: {self.successful_transaction_count}")
        self.transacted_amount_count_label = QLabel(f"Total successfully transacted: ${self.transacted_amount_count}")
        self.failed_transaction_count_label = QLabel(f"Total failed transactions: {self.failed_transaction_count}")
        self.declined_count_label = QLabel(f"Processor Declined transactions: {self.declined_count}")
        self.rejected_count_label = QLabel(f"Gateway Rejected transactions: {self.rejected_count}")
        self.failed_count_label = QLabel(f"Other transaction failures: {self.failed_count}")
        self.refunded_count_label = QLabel(f"Total refunds: {self.refunded_count}")
        self.total_refunded_label = QLabel(f"Total amount refunded: ${self.total_refunded}")
        self.average_transaction_amount_label = QLabel(f"Average transaction amount: ${self.average_transaction_amount}")
        self.credit_card_txns_label = QLabel(f"Credit card transactions: {self.credit_card_txns}")
        self.apple_pay_txns_label = QLabel(f"Apple Pay transactions: {self.apple_pay_txns}")
        self.google_pay_txns_label = QLabel(f"Google Pay transactions: {self.google_pay_txns}")
        self.paypal_txns_label = QLabel(f"PayPal transactions: {self.paypal_txns}") 

        layout = QVBoxLayout()
        layout.addWidget(self.successful_transaction_count_label)
        layout.addWidget(self.transacted_amount_count_label)
        layout.addWidget(self.failed_transaction_count_label)
        layout.addWidget(self.declined_count_label)
        layout.addWidget(self.rejected_count_label)
        layout.addWidget(self.failed_count_label)
        layout.addWidget(self.refunded_count_label)
        layout.addWidget(self.total_refunded_label)
        layout.addWidget(self.average_transaction_amount_label)
        layout.addWidget(self.credit_card_txns_label)
        layout.addWidget(self.apple_pay_txns_label)
        layout.addWidget(self.google_pay_txns_label)
        layout.addWidget(self.paypal_txns_label)

        self.setLayout(layout)

    def update_transaction_data(self, updated_data):
        self.successful_transaction_count = updated_data["successful_transaction_count"]["count"]
        self.transacted_amount_count = updated_data["transacted_amount"]["count"]
        self.failed_transaction_count = updated_data["failed_transaction_count"]["count"]
        self.declined_count = updated_data["declined_count"]["count"]
        self.rejected_count = updated_data["rejected_count"]["count"]
        self.failed_count = updated_data["failed_count"]["count"]
        self.refunded_count = updated_data["refunded_count"]["count"]
        self.total_refunded = updated_data["total_refunded"]["count"]
        self.average_transaction_amount = updated_data["average_transaction_amount"]["count"]
        self.credit_card_txns = updated_data["credit_card_txns"]["count"]
        self.apple_pay_txns = updated_data["apple_pay_txns"]["count"]
        self.google_pay_txns = updated_data["google_pay_txns"]["count"]
        self.paypal_txns = updated_data["paypal_txns"]["count"]

        self.successful_transaction_count_label.setText(f"Successful transactions: {self.successful_transaction_count}")
        self.transacted_amount_count_label.setText(f"Total successfully transacted: ${self.transacted_amount_count}")
        self.failed_transaction_count_label.setText(f"Total failed transactions: {self.failed_transaction_count}")
        self.declined_count_label.setText(f"Processor Declined transactions: {self.declined_count}")
        self.rejected_count_label.setText(f"Gateway Rejected transactions: {self.rejected_count}")
        self.failed_count_label.setText(f"Other transaction failures: {self.failed_count}")
        self.refunded_count_label.setText(f"Total refunds: {self.refunded_count}")
        self.total_refunded_label.setText(f"Total amount refunded: ${self.total_refunded}")
        self.average_transaction_amount_label.setText(f"Average transaction amount: ${self.average_transaction_amount}")
        self.credit_card_txns_label.setText(f"Credit card transactions: {self.credit_card_txns}")
        self.apple_pay_txns_label.setText(f"Apple Pay transactions: {self.apple_pay_txns}")
        self.google_pay_txns_label.setText(f"Google Pay transactions: {self.google_pay_txns}")
        self.paypal_txns_label.setText(f"PayPal transactions: {self.paypal_txns}") 
            

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

        # Initialize the gateway
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

        # Initialize the layout immediately so that it doesn't error out when called in the search function.
        self.layout = QVBoxLayout()

        # Creating start date and end date variables which will be plugged into the Transaction.search() call.
        self.start_date = start_date
        self.end_date = end_date

        # UPDATE: Streamlined everything so that all of the transaction searching happens in transaction_search().
        # Now in __init__(), we just calculate the search range, then pass it into the search function.
        if (self.start_date == None) and (self.end_date == None):
            
            # Calculating todays date and the date 30 days before todays date.
            # This will be immediately passed into a transaction.search() when the file is run.
            # This is so that the user can immediately see the stats for their transactions in the last 30 days.
            # If they want to search a new date range, they're free to do so with the calendar, but the last 30 days' data is immediately and quickly supplied.

            # Grab todays date using date().
            todayDate = date.today()
            # Format todays date into the format accepted by the transaction.search() call.
            todayDateFormatted = datetime(todayDate.year, todayDate.month, todayDate.day, 23, 59, 59)

            # Do the exact same thing to get 30 days ago's date, except take away 30 days.
            thirtyDaysAgo = date.today() - timedelta(days=30)
            thirtyDaysAgoFormatted = datetime(thirtyDaysAgo.year, thirtyDaysAgo.month, thirtyDaysAgo.day)

            self.datesWidget = DateWidget(thirtyDaysAgoFormatted, todayDateFormatted)
            self.transaction_search(thirtyDaysAgo, todayDate)
            
        else:
            # In this case, the dates have been provided via command line arguments.
            # They are provided as strings so we first convert them to datetime objects.
            startDate = datetime.strptime(self.start_date, "%m/%d/%Y")
            endDate = datetime.strptime(self.end_date, "%m/%d/%Y")
            endDate = endDate.replace(hour=23, minute=59, second=59)

            # We reset the self.dates variables back to None after we've done everything we need with them so that the calendar click functions properly.
            self.start_date = None
            self.end_date = None

            self.datesWidget = DateWidget(startDate, endDate)
            self.transaction_search(startDate, endDate)

        # Call handle_calendar_click function when the user clicks a date in the calendar.
        # UPDATE: Instead using the "clicked" handler here. Better allows for clicking the same date repeatedly.
        self.calendar.clicked.connect(self.handle_calendar_click)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    # Changing this function up a bit.
    def handle_calendar_click(self, date):
        # This function allows the user to enter the same date twice, so the user can search a single date if they want.
        # The start_date and end_date variables are initially set as None.
        # So first we check if start_date has a value.
        if not self.start_date:
            # If not, set it to whatever date was clicked.
            self.start_date = date
            print(f"Start date: {self.start_date}")
        else:
            # If it does, instead set the end_date to whatever date was clicked.
            self.end_date = date
            print(f"End date: {self.end_date}")

            # Call the functions to change the widget data with the new dates the user just selected.
            self.datesWidget.update_date_range(self.start_date, self.end_date)
            self.transaction_search(self.start_date, self.end_date)

            # Reset them both to None so that the user can run a new search in the same window.
            self.start_date = None
            self.end_date = None

    def transaction_search(self, startDate, endDate):
        if isinstance(startDate, QDate):
            startDateFormatted = datetime(startDate.year(), startDate.month(), startDate.day())
            endDateFormatted = datetime(endDate.year(), endDate.month(), endDate.day(), 23, 59, 59)
        else:
            startDateFormatted = datetime(startDate.year, startDate.month, startDate.day)
            endDateFormatted = datetime(endDate.year, endDate.month, endDate.day, 23, 59, 59)

        print(f"New start date: {startDateFormatted}")
        print(f"New end date: {endDateFormatted}")

        transaction_counts = {
            "successful_transaction_count": {"count": 0},
            "failed_transaction_count": {"count": 0},
            "declined_count": {"count": 0},
            "rejected_count": {"count": 0},
            "failed_count": {"count": 0},
            "refunded_count": {"count": 0},
            "transacted_amount": {"count": 0.00},
            "total_refunded": {"count": 0.00},
            "average_transaction_amount": {"count": 0.00},
            "credit_card_txns": {"count": 0},
            "apple_pay_txns": {"count": 0},
            "google_pay_txns": {"count": 0},
            "paypal_txns": {"count": 0}
        }

        transaction_average = 0.00

        collection = self.gateway.transaction.search(
          braintree.TransactionSearch.created_at.between(
            startDateFormatted,
            endDateFormatted
          )
        )

        for transaction in collection.items:
            # If the transaction  has a successful status, add to the success count in the dictionary.
            ## We also count the total amount processed and total successful transactions here.
            if (transaction.status in ("authorized", "submitted_for_settlement", "settling", "settled")) and (transaction.refunded_transaction_id == None):
                print("Success transaction ID: " + transaction.id)
                print("Payment method: " + transaction.payment_instrument_type)
                transaction_counts["successful_transaction_count"]["count"] += 1
                transaction_counts["transacted_amount"]["count"] += float(transaction.amount)
            # Counting processor declined transactions.
            elif transaction.status == "processor_declined":
                print("Processor Declined transaction ID: " + transaction.id)
                transaction_counts["failed_transaction_count"]["count"] += 1
                transaction_counts["declined_count"]["count"] += 1
            # Counting gateway rejected transactions.
            elif transaction.status == "gateway_rejected":
                print("Gateway Rejected transaction ID: " + transaction.id)
                transaction_counts["failed_transaction_count"]["count"] += 1
                transaction_counts["rejected_count"]["count"] += 1
            # Any other failed txn type gets tossed into these buckets.
            elif transaction.status in ("failed", "authorization_expired", "settlement_declined", "voided"):
                print("Failed transaction ID: " + transaction.id)
                transaction_counts["failed_transaction_count"]["count"] += 1
                transaction_counts["failed_count"]["count"] += 1

            # This is where we count the refund stats.
            ## UPDATE: Instead of searching for the refund IDs, now we just pull any refunds within this search range.
            ## That would be the case if a refunded_transaction_id exists
            if (transaction.refunded_transaction_id != None):
                # If so, we just add 1 to the refund count and add the amount of the transaction to the total amount refunded count.
                transaction_counts["refunded_count"]["count"] += 1
                transaction_counts["total_refunded"]["count"] += float(transaction.amount)

            # This is where we count the payment methods used.
            if (transaction.payment_instrument_type == "credit_card"):
                transaction_counts["credit_card_txns"]["count"] += 1
            elif (transaction.payment_instrument_type == "apple_pay_card"):
                transaction_counts["apple_pay_txns"]["count"] += 1
            elif (transaction.payment_instrument_type == "android_pay_card"):
                transaction_counts["google_pay_txns"]["count"] += 1
            elif (transaction.payment_instrument_type == "paypal_account"):
                transaction_counts["paypal_txns"]["count"] += 1

        # This is where we calculate the transaction average and add it to the dictionary.
        transaction_average = transaction_counts["transacted_amount"]["count"] / transaction_counts["successful_transaction_count"]["count"]
        rounded_transaction_average = round(transaction_average, 2)
        transaction_counts["average_transaction_amount"]["count"] += rounded_transaction_average

        print(transaction_counts)

        self.update_widget_data(transaction_counts)

    # This function now controls all of the adding and removing of widgets.
    def update_widget_data(self, new_data):
        # First we check if countWidget already exists, which would be the case if the user is running a new search after the initial one.
        # If so, call update_transaction_data which just updates the existing widget with the new data.
        if hasattr(self, 'countWidget'):
            self.countWidget.update_transaction_data(new_data)
        # If not, we create the widget with the data - the initial run.
        else:
            self.countWidget = TransactionWidget(new_data)
            
        # Then we add all of the widgets here. We don't need to wrap these statements in a conditional; if it's the first search, they're all added.
        ## If it's a repeat search, PyQt sees that the widgets already exist and so the addWidget() calls are essentially ignored.
        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.datesWidget)
        self.layout.addWidget(self.countWidget)


def convertToYYYY(date):
    if date and len(date.split('/')[2]) == 2:
        parts = date.split('/')
        parts[2] = "20" + parts[2]
        return '/'.join(parts)
    return date

def main():
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser(description="Transaction search")
    parser.add_argument("start_date", nargs="?", default=None, help="Start date (format: MM/DD/YYYY or MM/DD/YY))")
    parser.add_argument("end_date", nargs="?", default=None, help="End date (format: MM/DD/YYYY or MM/DD/YY))")
    args = parser.parse_args()

    args.start_date = convertToYYYY(args.start_date)
    args.end_date = convertToYYYY(args.end_date)

    window = MainWindow(args.start_date, args.end_date)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
