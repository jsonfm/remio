"""
A PyQt5 App which displays a single camera video.
"""
import sys
import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QImage
from remio import Mockup


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
        self.setWindowTitle('Camera viewer Example')
        self.setGeometry(100, 100, 800, 500)

        self.imageLabel1 = QImageLabel('Not available image')
        self.imageLabel2 = QImageLabel('Not available image')

        layout =  QHBoxLayout()
        layout.addWidget(self.imageLabel1)
        layout.addWidget(self.imageLabel2)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        # Configure Cameras
        self.fps = 30
        self.Mockup = Mockup(
                cameraDevices={
                           'webcam': 0, 
                           'mobile': 'http://192.168.100.56:3000/video/mjpeg'
                          }, 
                cameraOptions={
                        'fps': self.fps,
                        'size': None,
                        }
            )
        self.Mockup.start(camera=True)

        # Configure Timer
        self.timer = QTimer()   
        self.timer.timeout.connect(self.updateVideo)
        self.timer.start(1000 // 10)

    def updateVideo(self):
        """It updates video image on the GUI."""
        images = self.Mockup.camera.getAllFrames(asDict=False)
        for index in range(len(images)):
            image = images[index]
            if image is not None:
                imageLabel = getattr(self, f"imageLabel{index + 1}")
                imageLabel.setImage(image, scaledWidth=400, scaledHeight=600)
    

    def closeEvent(self, event):
        """When the app is closed, all process must be stopped."""
        self.Mockup.stop()


if __name__ == "__main__" :
  App = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(App.exec())