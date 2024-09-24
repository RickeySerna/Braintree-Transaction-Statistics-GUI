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

class TransactionSearchThread(QThread):
    search_completed = pyqtSignal()

    def __init__(self, start_date, end_date, search_function):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.search_function = search_function

    def run(self):
        self.search_function(self.start_date, self.end_date)
        self.search_completed.emit()
