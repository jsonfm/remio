"""A PyQt5 App which displays a single camera video."""
import sys
import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QImage
from remio import Camera

# Load settings
from .settings import settings


class QImageLabel(QLabel):
    """Custom QLabel with methods to display numpy arrays (opencv images)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def arrayToPixmap(self, array, width: int = 480, height: int = 600):
        """It converts an image array to a QPixmap format.

        :param array: image array
        :param width: scaled width
        :param width: scaled height
        """
        rgb = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytesPerLine = ch * w
        qimage = QImage(rgb.data, w, h, bytesPerLine, QImage.Format_RGB888)
        qimage = qimage.scaled(width, height, Qt.KeepAspectRatio)
        qpixmap = QPixmap.fromImage(qimage)
        return qpixmap

    def setImage(self, array, scaledWidth: int = 480, scaledHeight: int = 600):
        """It sets and image array over the label as QPixmap, to be displayed.

        :param array: image array
        :param scaledWidth: scaled width
        :param scaledHeight: scaled height
        """
        qimage = self.arrayToPixmap(array, width=scaledWidth, height=scaledHeight)
        self.setPixmap(qimage)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configure Window
        self.setWindowTitle("Camera viewer Example")
        self.setGeometry(100, 100, 500, 500)

        self.imageLabel = QImageLabel("Not available image")

        layout = QGridLayout()
        layout.addWidget(self.imageLabel, 0, 0)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        # Configure Cameras
        self.fps = 20
        self.camera = Camera(**settings)

        # Configure Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateVideo)
        self.timer.start(1000 // self.fps)

    def updateVideo(self):
        """It updates video image on the GUI."""
        image = self.camera.read()
        if image is not None:
            self.imageLabel.setImage(image)

    def closeEvent(self, event):
        """When the app is closed, all process must be stopped."""
        self.camera.stop()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(App.exec())
