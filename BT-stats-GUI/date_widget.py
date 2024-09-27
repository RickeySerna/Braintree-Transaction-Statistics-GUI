from datetime import date
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget
)


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

    def update_half_date_range(self, start_date):
        print(f"Start date inside update_half_date_range: {start_date}")

        start_python_date = date(start_date.year(), start_date.month(), start_date.day())
        formatted_start_date = start_python_date.strftime("%-m/%-d/%Y")

        print(f"Formatted start date: {formatted_start_date}")

        self.search_range.setText(f"Search range: {formatted_start_date} - ")
