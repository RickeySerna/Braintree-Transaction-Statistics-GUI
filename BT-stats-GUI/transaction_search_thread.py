from PyQt6.QtCore import QThread, pyqtSignal

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
