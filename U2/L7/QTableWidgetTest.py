from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
import sys

app = QApplication(sys.argv)
w = QMainWindow()
imgPath = "C:/Users/Marcus/Repos/AP-CSP/U2/L7/Cursorblade_banner.png"
img = QImage()
loaded = img.load(imgPath)

if loaded:
    # Resizing the image
    width = 150
    height = int(img.height() * width / img.width())
    img = img.scaled(width, height, Qt.KeepAspectRatio)

    thumbnailsWidget = QTableWidget()
    thumbnail = QTableWidgetItem()
    thumbnail.setData(Qt.DecorationRole, QPixmap.fromImage(img))

    thumbnailsWidget.setColumnCount(5)
    thumbnailsWidget.setRowCount(3)
    thumbnailsWidget.setItem(0, 0, thumbnail)

    w.setCentralWidget(thumbnailsWidget)
else:
    print("Image", imgPath, "was not opened!")

w.show()
sys.exit(app.exec())
