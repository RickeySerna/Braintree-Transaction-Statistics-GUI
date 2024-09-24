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

def convertToYYYY(date):
    # Split the date based on any slashes.
    parts = date.split('/')
    
    # Checking if the date is already in the YYYY format with the length of the third part being 4. If so, we just immediately return the date and end things there.
    # Also making sure that there are 3 parts to begin with, like a normal date.
    if len(parts) == 3 and len(parts[2]) == 4:
        return date
    # Checking if the date is in the MM/DD/YY format, with the third parts length being 2.
    elif len(parts) == 3 and len(parts[2]) == 2:
        # If so, we append "20" to the start of it.
        # We don't need to worry about 90s (or before) dates here since no such dates would contain BT transactions.
        parts[2] = "20" + parts[2]
        return '/'.join(parts)
    # If the else condition triggers, it means the value passed was not in the date format at all. So we raise a ValueError.
    else:
        raise ValueError("Invalid date(s) passed.")
