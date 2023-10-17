from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QProgressBar
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import os
from template_preprocess import ImagePreprocessor
from convert import OCRProcess
import pandas as pd

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
            img_front = OCRProcess.process_image(self.front_image_path, self.x_grid, self.y_grid)
            img_front = img_front[0:self.y_grid-1]
        else:
            img_front = []

        # Behind Image OCR
        if self.behind_image_path:
            self.update_progress.emit(50)
            img_behind = OCRProcess.process_image(self.behind_image_path, self.x_grid, self.y_grid)
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
        self.front_image_list = []
        self.front_current_index = 0
        self.behind_image_list = []
        self.behind_current_index = 0
        self.templates = ['template/t1.png', 'template/t2.png', 'template/t3.png', 'template/t4.png']
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)

        grid_layout = QGridLayout()
        grid_layout.setRowStretch(0, 3)
        grid_layout.setRowStretch(1, 7)

        self.front_button = QPushButton('Get front img folder', self)
        self.front_button.clicked.connect(lambda: self.load_images('front'))
        grid_layout.addWidget(self.front_button, 0, 0)

        self.front_prev_button = QPushButton('Previous', self)
        self.front_prev_button.clicked.connect(lambda: self.show_prev_image('front'))
        grid_layout.addWidget(self.front_prev_button, 0, 1)

        self.front_next_button = QPushButton('Next', self)
        self.front_next_button.clicked.connect(lambda: self.show_next_image('front'))
        grid_layout.addWidget(self.front_next_button, 0, 2)

        self.front_process_button = QPushButton('Preprocess', self)
        self.front_process_button.clicked.connect(lambda: self.process_image('front'))
        grid_layout.addWidget(self.front_process_button, 0, 3)

        self.front_image_label = QLabel(self)
        self.front_image_label.setScaledContents(True)
        grid_layout.addWidget(self.front_image_label, 1, 0, 1, 4)

        self.behind_button = QPushButton('Get behind img folder', self)
        self.behind_button.clicked.connect(lambda: self.load_images('behind'))
        grid_layout.addWidget(self.behind_button, 0, 4)

        self.behind_prev_button = QPushButton('Previous', self)
        self.behind_prev_button.clicked.connect(lambda: self.show_prev_image('behind'))
        grid_layout.addWidget(self.behind_prev_button, 0, 5)

        self.behind_next_button = QPushButton('Next', self)
        self.behind_next_button.clicked.connect(lambda: self.show_next_image('behind'))
        grid_layout.addWidget(self.behind_next_button, 0, 6)

        self.behind_process_button = QPushButton('Preprocess', self)
        self.behind_process_button.clicked.connect(lambda: self.process_image('behind'))
        grid_layout.addWidget(self.behind_process_button, 0, 7)

        self.behind_image_label = QLabel(self)
        self.behind_image_label.setScaledContents(True)
        grid_layout.addWidget(self.behind_image_label, 1, 4, 1, 4)

        self.setLayout(grid_layout)

        self.ocr_progress_bar = QProgressBar(self)
        grid_layout.addWidget(self.ocr_progress_bar, 2, 0, 1, 8)

        self.convert_button = QPushButton('Convert', self)
        self.convert_button.clicked.connect(self.start_ocr)
        grid_layout.addWidget(self.convert_button, 0, 8)
    def load_images(self, position):
        folder = QFileDialog.getExistingDirectory(self, f'Select {position} Image Folder')

        if folder:
            image_list = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

            if image_list:
                if position == 'front':
                    self.front_image_list = image_list
                    self.front_current_index = 0
                    self.show_image('front')
                else:
                    self.behind_image_list = image_list
                    self.behind_current_index = 0
                    self.show_image('behind')

    def show_image(self, position):
        if position == 'front' and self.front_image_list:
            image_path = self.front_image_list[self.front_current_index]
            self.front_image_label.setPixmap(QPixmap(image_path))
        elif position == 'behind' and self.behind_image_list:
            image_path = self.behind_image_list[self.behind_current_index]
            self.behind_image_label.setPixmap(QPixmap(image_path))

    def process_image(self, position):
        if position == 'front' and self.front_image_list:
            image_path = self.front_image_list[self.front_current_index]
            processed_img = ImagePreprocessor.process_image(image_path, self.templates)
            qimg = QImage(processed_img.data, processed_img.shape[1], processed_img.shape[0], QImage.Format_Indexed8)
            self.front_image_label.setPixmap(QPixmap.fromImage(qimg))
        elif position == 'behind' and self.behind_image_list:
            image_path = self.behind_image_list[self.behind_current_index]
            processed_img = ImagePreprocessor.process_image(image_path, self.templates)
            qimg = QImage(processed_img.data, processed_img.shape[1], processed_img.shape[0], QImage.Format_Indexed8)
            self.behind_image_label.setPixmap(QPixmap.fromImage(qimg))

    def start_ocr(self):
        if not self.front_image_list and not self.behind_image_list:
            QMessageBox.warning(self, 'Warning', 'Images not loaded!')
            return

        self.ocr_thread = OCRThread(self.front_image_list[self.front_current_index] if self.front_image_list else None,
                                    self.behind_image_list[self.behind_current_index] if self.behind_image_list else None)
        self.ocr_thread.update_progress.connect(self.update_ocr_progress)
        self.ocr_thread.start()

    def update_ocr_progress(self, progress):
        self.ocr_progress_bar.setValue(progress)

    def show_prev_image(self, position):
        if position == 'front' and self.front_image_list:
            self.front_current_index = (self.front_current_index - 1) % len(self.front_image_list)
            self.show_image('front')
        elif position == 'behind' and self.behind_image_list:
            self.behind_current_index = (self.behind_current_index - 1) % len(self.behind_image_list)
            self.show_image('behind')

    def show_next_image(self, position):
        if position == 'front' and self.front_image_list:
            self.front_current_index = (self.front_current_index + 1) % len(self.front_image_list)
            self.show_image('front')
        elif position == 'behind' and self.behind_image_list:
            self.behind_current_index = (self.behind_current_index + 1) % len(self.behind_image_list)
            self.show_image('behind')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageViewer()
    ex.show()
    sys.exit(app.exec_())
