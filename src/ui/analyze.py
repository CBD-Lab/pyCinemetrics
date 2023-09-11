from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (
    QDockWidget, QLabel, QDialog, QVBoxLayout
)
from PySide2.QtCore import Qt


class Analyze(QDockWidget):
    def __init__(self,parent,filename):
        super().__init__('Analyze', parent)
        self.parent = parent
        self.filename = filename
        self.parent.filename_changed.connect(self.on_filename_changed)
        self.init_analyze()

    def init_analyze(self):
        self.labelAnalyze = QLabel("", self)
        self.labelAnalyze.setGeometry(60, 20, 300,250)
        self.labelAnalyze.mousePressEvent = self.on_analyze_image_click
    def on_filename_changed(self,filename):
        self.labelAnalyze.setPixmap(QPixmap())

    def on_analyze_image_click(self, event):
        if event.button() == Qt.LeftButton:
            # 获取原始图片
            pixmap = QPixmap(self.parent.control.AnalyzeImgPath)
            if pixmap is not None:
                # 创建一个新的窗口来显示放大后的图片
                pixmap = pixmap.scaled(pixmap.width(), pixmap.height())
                # 创建一个新的对话框来显示放大后的图片
                zoomed_dialog = QDialog(self)
                layout = QVBoxLayout()
                zoomed_label = QLabel()
                zoomed_label.setPixmap(pixmap)
                layout.addWidget(zoomed_label)
                zoomed_dialog.setLayout(layout)
                zoomed_dialog.setWindowTitle('Zoomed Image')
                zoomed_dialog.exec_()  # 进入对话框的主事件循环
