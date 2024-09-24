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

class TransactionWidget(QWidget):
    def __init__(self, transaction_data):
        super(TransactionWidget, self).__init__()
        self.setAutoFillBackground(True)

        self.successful_transaction_count = transaction_data["successful_transaction_count"]["count"]
        self.transacted_amount_count = float(transaction_data["transacted_amount"]["count"])
        self.failed_transaction_count = transaction_data["failed_transaction_count"]["count"]
        self.declined_count = transaction_data["declined_count"]["count"]
        self.rejected_count = transaction_data["rejected_count"]["count"]
        self.failed_count = transaction_data["failed_count"]["count"]
        self.refunded_count = transaction_data["refunded_count"]["count"]
        self.total_refunded = float(transaction_data["total_refunded"]["count"])
        self.average_transaction_amount = float(transaction_data["average_transaction_amount"]["count"])
        self.credit_card_txns = transaction_data["credit_card_txns"]["count"]
        self.apple_pay_txns = transaction_data["apple_pay_txns"]["count"]
        self.google_pay_txns = transaction_data["google_pay_txns"]["count"]
        self.paypal_txns = transaction_data["paypal_txns"]["count"]

        self.transaction_stats = {
            "successful_transaction_count": {
                "label": QLabel(f"Successful transactions: {self.successful_transaction_count}"),
                "count": self.successful_transaction_count
            },
            "transacted_amount": {
                "label": QLabel(f"Total successfully transacted: ${self.transacted_amount_count:,.2f}"),
                "count": self.transacted_amount_count
            },
            "failed_transaction_count": {
                "label": QLabel(f"Total failed transactions: {self.failed_transaction_count}"),
                "count": self.failed_transaction_count
            },
            "declined_count": {
                "label": QLabel(f" - Processor Declined transactions: {self.declined_count}"),
                "count": self.declined_count
            },
            "rejected_count": {
                "label": QLabel(f" - Gateway Rejected transactions: {self.rejected_count}"),
                "count": self.rejected_count
            },
            "failed_count": {
                "label": QLabel(f" - Other transaction failures: {self.failed_count}"),
                "count": self.failed_count
            },
            "refunded_count": {
                "label": QLabel(f"Total refunds: {self.refunded_count}"),
                "count": self.refunded_count
            },
            "total_refunded": {
                "label": QLabel(f"Total amount refunded: ${self.total_refunded:,.2f}"),
                "count": self.total_refunded
            },
            "average_transaction_amount": {
                "label": QLabel(f"Average transaction amount: ${self.average_transaction_amount:,.2f}"),
                "count": self.average_transaction_amount
            },
            "credit_card_txns": {
                "label": QLabel(f"Credit card transactions: {self.credit_card_txns}"),
                "count": self.credit_card_txns
            },
            "apple_pay_txns": {
                "label": QLabel(f"Apple Pay transactions: {self.apple_pay_txns}"),
                "count": self.apple_pay_txns
            },
            "google_pay_txns": {
                "label": QLabel(f"Google Pay transactions: {self.google_pay_txns}"),
                "count": self.google_pay_txns
            },
            "paypal_txns": {
                "label": QLabel(f"PayPal transactions: {self.paypal_txns}"),
                "count": self.paypal_txns
            }
        }

        layout = QVBoxLayout()

        for key, value in self.transaction_stats.items():
            layout.addWidget(value["label"])

        self.setLayout(layout)

    def update_transaction_data(self, updated_data):
        for key, value in self.transaction_stats.items():
            value["count"] = updated_data[key]["count"]
            current_text = value["label"].text()
            match = re.match(r"^(.*: \$?)", current_text)
            if match:
                initial_text = match.group(1)
                if '$' in initial_text:
                    formatted_value = f"{float(value['count']):,.2f}"
                else:
                    formatted_value = value['count']
                value["label"].setText(f"{initial_text}{formatted_value}")
