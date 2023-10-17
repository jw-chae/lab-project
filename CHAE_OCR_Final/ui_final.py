from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QMessageBox, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import os
import cv2
import numpy as np
from preprocess import ImagePreprocessor
from convert import OCRProcess
import pandas as pd

class CaptureThread(QThread):
    image_captured = pyqtSignal(str)

    def __init__(self, camera_id, output_folder):
        super().__init__()
        self.camera_id = camera_id
        self.output_folder = output_folder

    def run(self):
        cap = cv2.VideoCapture(self.camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1900)  # Set the resolution to 1920x1080
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1072)
        ret, frame = cap.read()
        if ret:
            # Crop the frame
            if self.camera_id == 701:
                height, _, _ = frame.shape
                frame = frame[int(height * 0.4):]
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)
            img_path = os.path.join(self.output_folder, f'{self.camera_id}.jpg')
            cv2.imwrite(img_path, frame)
            self.image_captured.emit(img_path)
        cap.release()

class PreprocessThread(QThread):
    image_preprocessed = pyqtSignal(str, str)

    def __init__(self, image_path, templates):
        super().__init__()
        self.image_path = image_path
        self.templates = templates

    def run(self):
        img = ImagePreprocessor.preprocess(self.image_path, self.templates)
        preprocessed_img_path = self.image_path.replace('.jpg', '_preprocessed.jpg')
        cv2.imwrite(preprocessed_img_path, img)
        self.image_preprocessed.emit(self.image_path, preprocessed_img_path)


def start_preprocessing(self):
    if not os.path.exists('images/img_front') and not os.path.exists('images/img_behind'):
        QMessageBox.warning(self, 'Warning', 'Images not captured!')
        return

    front_templates = ['template/t5.png','template/t6.png','template/t7.png','template/t8.png']
    behind_templates = ['template/t1.png', 'template/t2.png', 'template/t3.png', 'template/t4.png']

    front_image_path = os.path.join('images/img_front', '700.jpg') if os.path.exists('images/img_front') else None
    behind_image_path = os.path.join('images/img_behind', '701.jpg') if os.path.exists('images/img_behind') else None

    if front_image_path:
        self.front_preprocess_thread = PreprocessThread(front_image_path, front_templates)
        self.front_preprocess_thread.image_preprocessed.connect(self.show_preprocessed_image)
        self.front_preprocess_thread.start()

    if behind_image_path:
        self.behind_preprocess_thread = PreprocessThread(behind_image_path, behind_templates)
        self.behind_preprocess_thread.image_preprocessed.connect(self.show_preprocessed_image)
        self.behind_preprocess_thread.start()

class OCRThread(QThread):
    update_progress = pyqtSignal(int)

    def __init__(self, front_image_path, behind_image_path, x_grid=8, y_grid=16):
        super().__init__()
        self.front_image_path = front_image_path
        self.behind_image_path = behind_image_path
        self.x_grid = x_grid
        self.y_grid = y_grid

    def run(self):
        # Front Image OCR
        if self.front_image_path:
            self.update_progress.emit(25)
            img_front = OCRProcess.process_image(self.front_image_path, self.x_grid, 14)
            img_front = img_front[0:self.y_grid-1]
        else:
            img_front = []

        # Behind Image OCR
        if self.behind_image_path:
            self.update_progress.emit(50)
            img_behind = OCRProcess.process_image(self.behind_image_path, self.x_grid, 16)
            img_behind = img_behind[self.y_grid-15:]
        else:
            img_behind = []

        # Combine Results and Convert to CSV
        self.update_progress.emit(75)
        combined_img = img_front + img_behind
        df = pd.DataFrame(combined_img)
        df.to_csv('ocr_output_combined.csv', index=False, header=False)

        self.update_progress.emit(100)

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'OCR Converter'
        self.grid_size = 800  # Here we set the grid_size value
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)

        grid_layout = QGridLayout()
        grid_layout.setRowStretch(0, 3)
        grid_layout.setRowStretch(1, 7)

        self.front_capture_button = QPushButton('Capture Front Image', self)
        self.front_capture_button.clicked.connect(lambda: self.capture_image(700, 'images/img_front'))
        grid_layout.addWidget(self.front_capture_button, 0, 0)

        self.front_image_label = QLabel(self)
        self.front_image_label.setScaledContents(True)
        grid_layout.addWidget(self.front_image_label, 1, 0, 1, 2)

        self.behind_capture_button = QPushButton('Capture Behind Image', self)
        self.behind_capture_button.clicked.connect(lambda: self.capture_image(701, 'images/img_behind'))
        grid_layout.addWidget(self.behind_capture_button, 0, 2)

        self.behind_image_label = QLabel(self)
        self.behind_image_label.setScaledContents(True)
        grid_layout.addWidget(self.behind_image_label, 1, 2, 1, 2)

        self.ocr_progress_bar = QProgressBar(self)
        grid_layout.addWidget(self.ocr_progress_bar, 2, 0, 1, 4)

        self.convert_button = QPushButton('Convert', self)
        self.convert_button.clicked.connect(self.start_preprocessing)
        grid_layout.addWidget(self.convert_button, 0, 3)

        self.setLayout(grid_layout)

    def capture_image(self, camera_id, output_folder):
        self.capture_thread = CaptureThread(camera_id, output_folder)
        self.capture_thread.image_captured.connect(self.show_captured_image)
        self.capture_thread.start()

    def show_captured_image(self, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.grid_size, self.grid_size, Qt.KeepAspectRatio)  # Resize the image
        if 'img_front' in image_path:
            self.front_image_label.setPixmap(pixmap)
        else:
            self.behind_image_label.setPixmap(pixmap)

    def start_preprocessing(self):
        if not os.path.exists('images/img_front') and not os.path.exists('images/img_behind'):
            QMessageBox.warning(self, 'Warning', 'Images not captured!')
            return

        front_templates = ['template/t5.png','template/t6.png','template/t7.png','template/t8.png']
        behind_templates = ['template/t1.png', 'template/t2.png', 'template/t3.png', 'template/t4.png']
        front_image_path = os.path.join('images/img_front', '700.jpg') if os.path.exists('images/img_front') else None
        behind_image_path = os.path.join('images/img_behind', '701.jpg') if os.path.exists('images/img_behind') else None

        if front_image_path:
            self.front_preprocess_thread = PreprocessThread(front_image_path, front_templates)
            self.front_preprocess_thread.image_preprocessed.connect(self.show_preprocessed_image)
            self.front_preprocess_thread.start()

        if behind_image_path:
            self.behind_preprocess_thread = PreprocessThread(behind_image_path, behind_templates)
            self.behind_preprocess_thread.image_preprocessed.connect(self.show_preprocessed_image)
            self.behind_preprocess_thread.start()

    def show_preprocessed_image(self, image_path):
        if 'img_front' in image_path:
            self.front_image_label.setPixmap(QPixmap(image_path))
        else:
            self.behind_image_label.setPixmap(QPixmap(image_path))

        self.start_ocr()

    def start_ocr(self):
        front_image_path = os.path.join('images/img_front', '700_preprocessed.jpg') if os.path.exists('images/img_front') else None
        behind_image_path = os.path.join('images/img_behind', '701_preprocessed.jpg') if os.path.exists('images/img_behind') else None

        self.ocr_thread = OCRThread(front_image_path, behind_image_path)
        self.ocr_thread.update_progress.connect(self.update_ocr_progress)
        self.ocr_thread.start()

    def update_ocr_progress(self, progress):
        self.ocr_progress_bar.setValue(progress)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageViewer()
    ex.show()
    sys.exit(app.exec_())
