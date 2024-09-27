import braintree
import sys
import os
from dotenv import load_dotenv
#from braintree.exceptions import *
from datetime import datetime
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QCalendarWidget,
    QStatusBar
)
from .error_message_box import ErrorMessageBox
from .date_widget import DateWidget
from .transaction_widget import TransactionWidget
from .transaction_search_thread import TransactionSearchThread



class MainWindow(QMainWindow):
    def __init__(self, start_date=None, end_date=None):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Braintree Transaction Statistics")


        load_dotenv()
        MERCHANT_ID = os.getenv('MERCHANT_ID')
        PUBLIC_KEY = os.getenv('PUBLIC_KEY')
        PRIVATE_KEY = os.getenv('PRIVATE_KEY')
        ENVIRONMENT = os.getenv('ENVIRONMENT')

        environment_map = {
            'Sandbox': braintree.Environment.Sandbox,
            'Production': braintree.Environment.Production,
        }

        # Initializing the gateway.
        try:
            self.gateway = braintree.BraintreeGateway(
              braintree.Configuration(
                  environment_map[ENVIRONMENT],
                  merchant_id=MERCHANT_ID,
                  public_key=PUBLIC_KEY,
                  private_key=PRIVATE_KEY
              )
            )
        except:
            dlg = ErrorMessageBox()
            dlg.update_box_message("Please enter your API keys in the file.")
            dlg.update_box_title("API Key Error")
            dlg.exec()
            sys.exit(1)

        # Creating the status bar to be used to let the user know when a new search is running.
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Creating a calendar widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setMinimumDate(QDate(2000, 1, 1))
        self.calendar.setMaximumDate(QDate(2099, 12, 31))
        self.calendar.hide()

        self.toggle_calendar_button = QPushButton("Show Calendar", self)
        self.toggle_calendar_button.clicked.connect(self.toggle_calendar)

        # Initialize the layout immediately so that it doesn't error out when called in the search function.
        widget = QWidget()
        self.setCentralWidget(widget)
        self.layout = QVBoxLayout(widget)        

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

    # Changing this function up a bit.
    def handle_calendar_click(self, date):
        # This function allows the user to enter the same date twice, so the user can search a single date if they want.
        # The start_date and end_date variables are initially set as None.
        # So first we check if start_date has a value.
        if not self.start_date:
            # If not, set it to whatever date was clicked.
            self.start_date = date
            print(f"Start date: {self.start_date}")
            self.datesWidget.update_half_date_range(self.start_date)
        else:

            result = date >= self.start_date
            print(f"End date greater than or equal to start date?: {result}")
            # If it does, instead set the end_date to whatever date was clicked.
            if (date >= self.start_date): 
                self.end_date = date
                print(f"End date: {self.end_date}")

                self.datesWidget.update_date_range(self.start_date, self.end_date)

                # Call the functions to change the widget data with the new dates the user just selected.
                self.status_bar.showMessage("Searching for transactions...")
                
                self.search_thread = TransactionSearchThread(self.start_date, self.end_date, self.transaction_search)
                self.search_thread.search_completed.connect(self.on_search_completed)
                self.search_thread.start()
            else:
                dlg = ErrorMessageBox(self)
                dlg.exec()


    def on_search_completed(self):
        self.status_bar.clearMessage()

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

        try:
            collection = self.gateway.transaction.search(
              braintree.TransactionSearch.created_at.between(
                startDateFormatted,
                endDateFormatted
              )
            )
        except:
            dlg = ErrorMessageBox()
            dlg.update_box_message("There was an error connecting to Braintree. Please ensure your API keys are valid or try again later.")
            dlg.update_box_title("Braintree Search Error")
            dlg.exec()
            sys.exit(1)

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
        # UPDATE: Adding a check here to see if the successful txn count is 0.
        # If it is, we just define transaction_average as 0 to avoid any divide by 0 errors.
        if (transaction_counts["successful_transaction_count"]["count"] != 0):
            transaction_average = round(transaction_counts["transacted_amount"]["count"] / transaction_counts["successful_transaction_count"]["count"], 2)
        else:
            transaction_average = 0
        
        # Also forcing the values to be displayed with two decimal places, even if they're 0. We do this for all three values representing money.
        transaction_counts["average_transaction_amount"]["count"] = f'{transaction_average:.2f}'
        
        # Also cutting the total amount transacted to the hundredths place.
        transaction_counts["transacted_amount"]["count"] = f'{round(transaction_counts["transacted_amount"]["count"], 2):.2f}'
        transaction_counts["total_refunded"]["count"] = f'{transaction_counts["total_refunded"]["count"]:.2f}'

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
        self.layout.addWidget(self.toggle_calendar_button)
        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.datesWidget)
        self.layout.addWidget(self.countWidget)
        self.status_bar.clearMessage()

    def toggle_calendar(self):
        if self.calendar.isVisible():
            self.calendar.hide()
            self.toggle_calendar_button.setText("Show Calendar")
        else:
            self.calendar.show()
            self.toggle_calendar_button.setText("Hide Calendar")
