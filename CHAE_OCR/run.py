import sys
import glob
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel,\
QPushButton,QLineEdit,QVBoxLayout, QWidget,QGroupBox,QGridLayout,QHBoxLayout\
,QSizePolicy,QMessageBox


from preprocess import ImagePreprocessor

class ImageProcessingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left_top = (0.05, 0.05)
        self.right_top = (0.98, 0.05)
        self.left_bottom = (0, 1)
        self.right_bottom = (1, 1)
        self.threshold = 200
        self.setGeometry(300, 300, 400, 300)
        self.title = 'Image Processing GUI'
        self.image = ""  # Initialize self.image attribute
        self.image_index = 0  # Initialize self.image_index attribute
        self.images = []  # Initialize self.images attribute
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow the main window to be resized

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()


        # Create labels and textboxes
        self.lbl_left_top = QLabel('Left Top: X, Y')
        self.txt_left_top_x = QLineEdit(self)
        self.txt_left_top_y = QLineEdit(self)

        self.lbl_right_top = QLabel('Right Top: X, Y')
        self.txt_right_top_x = QLineEdit(self)
        self.txt_right_top_y = QLineEdit(self)

        self.lbl_left_bottom = QLabel('Left Bottom: X, Y')
        self.txt_left_bottom_x = QLineEdit(self)
        self.txt_left_bottom_y = QLineEdit(self)

        self.lbl_right_bottom = QLabel('Right Bottom: X, Y')
        self.txt_right_bottom_x = QLineEdit(self)
        self.txt_right_bottom_y = QLineEdit(self)

        self.lbl_threshold = QLabel('Threshold')
        self.txt_threshold = QLineEdit(self)

        # Create layout for left top coordinate and add widgets for right top, left bottom and right bottom
        hBox_left_top = QHBoxLayout()
        hBox_left_top.addWidget(self.lbl_left_top)
        self.txt_left_top_x.setFixedWidth(50)
        self.txt_left_top_y.setFixedWidth(50)
        self.txt_left_top_x.setFixedHeight(20)
        self.txt_left_top_y.setFixedHeight(20)
        hBox_left_top.addWidget(self.txt_left_top_x)
        hBox_left_top.addWidget(self.txt_left_top_y)
        self.txt_left_top_x.setText(str(self.left_top[0]))
        self.txt_left_top_y.setText(str(self.left_top[1]))
        vbox.addLayout(hBox_left_top)

        hBox_right_top = QHBoxLayout()
        hBox_right_top.addWidget(self.lbl_right_top)
        self.txt_right_top_x.setFixedWidth(50)
        self.txt_right_top_y.setFixedWidth(50)
        self.txt_right_top_x.setFixedHeight(20)
        self.txt_right_top_y.setFixedHeight(20)
        hBox_right_top.addWidget(self.txt_right_top_x)
        hBox_right_top.addWidget(self.txt_right_top_y)
        self.txt_right_top_x.setText(str(self.right_top[0]))
        self.txt_right_top_y.setText(str(self.right_top[1]))
        vbox.addLayout(hBox_right_top)

        hBox_left_bottom = QHBoxLayout()
        hBox_left_bottom.addWidget(self.lbl_left_bottom)
        self.txt_left_bottom_x.setFixedWidth(50)
        self.txt_left_bottom_y.setFixedWidth(50)
        self.txt_left_bottom_x.setFixedHeight(20)
        self.txt_left_bottom_y.setFixedHeight(20)
        hBox_left_bottom.addWidget(self.txt_left_bottom_x)
        hBox_left_bottom.addWidget(self.txt_left_bottom_y)
        self.txt_left_bottom_x.setText(str(self.left_bottom[0]))
        self.txt_left_bottom_y.setText(str(self.left_bottom[1]))
        vbox.addLayout(hBox_left_bottom)

        hBox_right_bottom = QHBoxLayout()
        hBox_right_bottom.addWidget(self.lbl_right_bottom)
        self.txt_right_bottom_x.setFixedWidth(50)
        self.txt_right_bottom_y.setFixedWidth(50)
        self.txt_right_bottom_x.setFixedHeight(20)
        self.txt_right_bottom_y.setFixedHeight(20)
        hBox_right_bottom.addWidget(self.txt_right_bottom_x)
        hBox_right_bottom.addWidget(self.txt_right_bottom_y)
        self.txt_right_bottom_x.setText(str(self.right_bottom[0]))
        self.txt_right_bottom_y.setText(str(self.right_bottom[1]))
        vbox.addLayout(hBox_right_bottom)
        
        hBox_threshold = QHBoxLayout()
        hBox_threshold.addWidget(self.lbl_threshold)
        self.txt_threshold.setFixedWidth(50)
        self.txt_threshold.setFixedHeight(20)
        hBox_threshold.addWidget(self.txt_threshold)
        self.txt_threshold.setText(str(self.threshold))
        vbox.addLayout(hBox_threshold)



        # Create apply button set button size is 100x30
        self.btn_apply = QPushButton('Apply', self)
        self.btn_apply.clicked.connect(self.onClicked)
        self.btn_apply.setFixedSize(100, 30)
        # Add labels and textboxes to the layout
        # vbox.addWidget(self.lbl_left_top)
        # vbox.addWidget(self.txt_left_top_x)
        # vbox.addWidget(self.txt_left_top_y)

        # vbox.addWidget(self.lbl_right_top)
        # vbox.addWidget(self.txt_right_top_x)
        # vbox.addWidget(self.txt_right_top_y)

        # vbox.addWidget(self.lbl_left_bottom)
        # vbox.addWidget(self.txt_left_bottom_x)
        # vbox.addWidget(self.txt_left_bottom_y)

        # vbox.addWidget(self.lbl_right_bottom)
        # vbox.addWidget(self.txt_right_bottom_x)
        # vbox.addWidget(self.txt_right_bottom_y)

        vbox.addWidget(self.btn_apply)

        # Create grid layout and add it to vbox
        self.createGridLayout()
        vbox.addWidget(self.horizontalGroupBox)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        # Add widgets to the layout
        # Configure the buttons and connect to their respective slots
        self.loadBtn = QPushButton('Load', self)
        self.loadBtn.clicked.connect(self.loadImages)
        layout.addWidget(self.loadBtn, 0, 0)

        self.prevBtn = QPushButton('Prev', self)
        self.prevBtn.clicked.connect(self.prevImage)
        layout.addWidget(self.prevBtn, 1, 0)

        self.nextBtn = QPushButton('Next', self)
        self.nextBtn.clicked.connect(self.nextImage)
        layout.addWidget(self.nextBtn, 2, 0)

        self.processBtn = QPushButton('Process', self)
        self.processBtn.clicked.connect(self.processImage)
        layout.addWidget(self.processBtn, 3, 0)

        self.imageLabel = QLabel(self)
        self.imageLabel.setPixmap(QPixmap(self.image))
        layout.addWidget(self.imageLabel, 0, 1, 4, 1)

        # Image Label
        self.imageLabel = QLabel(self)
        self.imageLabel.setPixmap(QPixmap(self.image))
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setMinimumSize(1, 1)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)  # Allow the image label to be resized

            # Add Image Label to the layout
        layout.addWidget(self.imageLabel, 0, 1, 5, 1)

        # Set stretch factors
        layout.setColumnStretch(0, 3)  # 30% of space is reserved for buttons and textbox
        layout.setColumnStretch(1, 7)  # 70% of space is reserved for image label

        # Set layout to the QWidget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.horizontalGroupBox.setLayout(layout)
    
    def onClicked(self):
        # Get values from textboxes
        self.left_top_x = float(self.txt_left_top_x.text())
        self.left_top_y = float(self.txt_left_top_y.text())

        self.right_top_x = float(self.txt_right_top_x.text())
        self.right_top_y = float(self.txt_right_top_y.text())

        self.left_bottom_x = float(self.txt_left_bottom_x.text())
        self.left_bottom_y = float(self.txt_left_bottom_y.text())

        self.right_bottom_x = float(self.txt_right_bottom_x.text())
        self.right_bottom_y = float(self.txt_right_bottom_y.text())

        self.threshold = int(self.txt_threshold.text())  # assuming threshold is an integer

        # Apply the data
        # Check if image is loaded
        if self.image is not "":
            # Draw circles at specified points
            img_height, img_width = self.image.shape[:2]
            
            # Calculate the coordinates based on the image's width and height
            left_top = (int(self.left_top_x * img_width), int(self.left_top_y * img_height))
            right_top = (int(self.right_top_x * img_width), int(self.right_top_y * img_height))
            left_bottom = (int(self.left_bottom_x * img_width), int(self.left_bottom_y * img_height))
            right_bottom = (int(self.right_bottom_x * img_width), int(self.right_bottom_y * img_height))

            # Draw the circles
            cv2.circle(self.image, left_top, 5, (255,0,0), -1)
            cv2.circle(self.image, right_top, 5, (255,0,0), -1)
            cv2.circle(self.image, left_bottom, 5, (255,0,0), -1)
            cv2.circle(self.image, right_bottom, 5, (255,0,0), -1)

            # Convert OpenCV image to QImage and display it on the QLabel
            rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
            self.imageLabel.setPixmap(QPixmap.fromImage(p))
        
        QMessageBox.information(self, "Info", "Data Applied!")


    def loadImages(self):
        fname = QFileDialog.getExistingDirectory(self, 'Open directory', './')
        self.images = glob.glob(fname + '/*.jpg')
        if self.images:
            self.image = cv2.imread(self.images[0])
            self.showImage()


    def prevImage(self):
        if not self.images:
            QMessageBox.warning(self, "Warning", "Image Unloaded")
            return
        if self.images:
            self.image_index = (self.image_index - 1) % len(self.images)
            self.showImage(self.images[self.image_index])

    def nextImage(self):
        if not self.images:
            QMessageBox.warning(self, "Warning", "Image Unloaded")
            return

        if self.images:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.showImage(self.images[self.image_index])

    def processImage(self):
        if not self.images:
            QMessageBox.warning(self, "Warning", "Image Unloaded")
            return

        if self.images:
            # Get coordinates from attributes set in onClicked
            self.left_top = (self.left_top_x, self.left_top_y)
            self.right_top = (self.right_top_x, self.right_top_y)
            self.left_bottom = (self.left_bottom_x, self.left_bottom_y)
            self.right_bottom = (self.right_bottom_x, self.right_bottom_y)

            # Use the coordinates
            result = ImagePreprocessor.process_image(
                self.images[self.image_index], self.left_top, self.right_top, self.left_bottom,\
                        self.right_bottom, self.threshold)  #, left_top, right_top, left_bottom, right_bottom 
        # Update QLineEdit with the returned coordinates
        self.txt_left_top_x.setText(str(self.left_top[0]))
        self.txt_left_top_y.setText(str(self.left_top[1]))
        self.txt_right_top_x.setText(str(self.right_top[0]))
        self.txt_right_top_y.setText(str(self.right_top[1]))
        self.txt_left_bottom_x.setText(str(self.left_bottom[0]))
        self.txt_left_bottom_y.setText(str(self.left_bottom[1]))
        self.txt_right_bottom_x.setText(str(self.right_bottom[0]))
        self.txt_right_bottom_y.setText(str(self.right_bottom[1]))

        self.showImage(result)

    def showImage(self, image_path=None):
        if isinstance(image_path, str):  # Check if image_path is a string
            self.image = cv2.imread(image_path)
        elif isinstance(image_path, np.ndarray):  # Check if the image_path is a numpy array
            self.image = image_path

        if self.image is not None and isinstance(self.image, np.ndarray):  # Check if self.image is not None and it's a numpy array
            height, width, channel = self.image.shape
            bytesPerLine = 3 * width
            # We should convert the colorspace of the image because in OpenCV, it's BGR but in Qt, it's RGB.
            image_to_show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            qImg = QImage(image_to_show.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.imageLabel.setPixmap(QPixmap.fromImage(qImg))



def main():
    app = QApplication(sys.argv)
    ex = ImageProcessingGUI()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

    def preprocessing(self):
        # Call your preprocessing function here
        print('Preprocessing')

    def readOCR(self):
        # Call your OCR function here
        print('READ_OCR')

    def save(self):
        # Call your save function here
        print('Save')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            self.nextImage()
        elif e.key() == Qt.Key_Left:
            self.prevImage()