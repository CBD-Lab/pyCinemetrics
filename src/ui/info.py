from PySide2.QtWidgets import (
    QDockWidget, QTableWidget, QTableWidgetItem
)
from PySide2.QtCore import Signal
import os
import cv2


class Info(QDockWidget):
    video_info_loaded = Signal(list)

    def __init__(self, parent):
        super().__init__('Info', parent)
        self.parent = parent
        self.init_ui()
        self.parent.filename.connect(self.on_filename_changed)
        self.video_info_loaded.connect(self.update_table)

    def init_ui(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Property', 'Value'])
        self.setWidget(self.table)

    def on_filename_changed(self, filename):
        self.table.setRowCount(0)
        self.parent.threadpool.submit(self.load_video_info, filename)

    def load_video_info(self, filename):
        video = cv2.VideoCapture(filename)
        if not video.isOpened():
            return

        properties = [
            ('File', os.path.basename(filename)),
            ('Frame count', int(video.get(cv2.CAP_PROP_FRAME_COUNT))),
            ('FPS', video.get(cv2.CAP_PROP_FPS)),
            ('Width', int(video.get(cv2.CAP_PROP_FRAME_WIDTH))),
            ('Height', int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))),
        ]

        video.release()

        self.video_info_loaded.emit(properties)

    def update_table(self, properties):
        self.table.setRowCount(0)

        for i, (prop, value) in enumerate(properties):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(prop))
            self.table.setItem(i, 1, QTableWidgetItem(str(value)))
