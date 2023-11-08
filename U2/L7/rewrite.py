import os
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon, QPixmap, QImage
from PySide6.QtCore import Qt

class Wishlister(QWidget):
    def __init__(self):
        super().__init__()
        self.app = QApplication([])
        self.wishlist_display = QTableWidget()
        self.database = []
        self.init_ui()

    def init_ui(self):
        self.wishlist_display.setColumnCount(5)
        self.wishlist_display.setHorizontalHeaderLabels(["#", "Banner", "Name", "Price", "URL"])

        if not os.path.exists(f"{os.path.dirname(__file__)}/storage"):
            os.mkdir(f"{os.path.dirname(__file__)}/storage")

        self.wishlist_display.show()