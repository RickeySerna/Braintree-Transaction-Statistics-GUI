import braintree
import datetime
import sys
import argparse
import math
import re
from braintree.exceptions import *
from datetime import date, datetime, timedelta
from PyQt6.QtCore import QDate, Qt, QThread, pyqtSignal
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
    QCalendarWidget,
    QStatusBar,
    QDialog,
    QDialogButtonBox
)
from dotenv import load_dotenv
import os
from .transaction_widget import TransactionWidget
from .transaction_search_thread import TransactionSearchThread
from .date_widget import DateWidget
from .error_message_box import ErrorMessageBox
from .main_window import MainWindow
from .utils import convertToYYYY


def main():
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser(description="Transaction search")
    parser.add_argument("arg1", nargs="?", default=None, help="Start date (format: MM/DD/YYYY or MM/DD/YY) or number of days from today")
    parser.add_argument("arg2", nargs="?", default=None, help="End date (format: MM/DD/YYYY or MM/DD/YY)")

    try:
        # First we check for the amount of arguments passed. If they provided more than two, we throw a ValueError right off the bat.
        if len(sys.argv) > 3:
            raise ValueError("Too many arguments")

        args = parser.parse_args()

        start_date_str = None
        end_date_str = None

        # In this flow, the user only provided 1 argument; a single integer telling the function how many days back the search should go from todays date.
        if args.arg1 is not None and args.arg2 is None:                
            # Store the days to search back in a variable.
            days = int(args.arg1)

            # Checking if the user entered a negative number. We throw an error if they did that will be caught later.
            if (days < 0):
                raise ValueError("Negative int")

            # Store todays date as the end date of the search.
            end_date = datetime.today()

            # Set the starting date of the search to todays date minus however many days the user entered.
            start_date = end_date - timedelta(days=days)

            # Format the dates properly.
            start_date_str = start_date.strftime("%m/%d/%Y")
            end_date_str = end_date.strftime("%m/%d/%Y")
            
        # In this flow, the user entered two dates and so we just pass those into the conversion function to be formatted properly.
        elif args.arg1 is not None and args.arg2 is not None:
            start_date_str = convertToYYYY(args.arg1)
            end_date_str = convertToYYYY(args.arg2)

            # Converting to date objects so that we can compare them.
            startDatetime = datetime.strptime(start_date_str, '%m/%d/%Y').date()
            endDatetime = datetime.strptime(end_date_str, '%m/%d/%Y').date()

            # Checking if the user entered a start date that is after the end date. If they did, we throw an error that will be caught in the except block.
            if (startDatetime > endDatetime):
                raise ValueError("Start date greater than end date")
            
        # If neither flow triggered, the user provided 0 arguments so we use the default behavior. Just submit the dates as NoneTypes and that'll be used to search the last 30 days in MainWindow.


        # Whatever happened to the date strings, now pass them into MainWindow().
        window = MainWindow(start_date_str, end_date_str)
        window.show()
    except ValueError as e:
        dlg = ErrorMessageBox()
        dlg.update_box_title("Date Input Error")
        
        # We check for the message passed in ValueError. If it's a message with converting an int, then the error was with flow 1 so we use that error message.
        if "invalid literal for int()" in str(e):
            dlg.update_box_message("Invalid integer passed.")
        # Checking for the negative int error thrown above.
        elif "Negative int" in str(e):
            dlg.update_box_message("The integer cannot be below 0.")
        # If instead it's the message indicating too many arguments, then the initial if condition was triggered and we set the error message accordingly.
        elif "Too many arguments" in str(e):
            dlg.update_box_message("Too many arguments. Please provide no more than two.")
        # If this is the error, then the user entered valid date strings, however the end date was before the start date.
        elif "Start date greater than end date" in str(e):
            # In this case, the default message already explains the error. So we just pass without updating the message.
            pass
        # Otherwise, the error must have been with one of the dates from flow 2 so we use that error message instead.
        else:
            dlg.update_box_message("Invalid date(s) passed.")
        
        dlg.exec()
        sys.exit(1)
            
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
