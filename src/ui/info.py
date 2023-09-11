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
        self.parent.filename_changed.connect(self.on_filename_changed)
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
        frame_path = self.frame_save = "./img/"+str(os.path.basename(filename)[0:-4])+"/frame"#图片存储路径  # 替换为您要检查的文件夹路径
        shot_count = 0

        # 使用os.listdir遍历文件夹中的所有项目（包括文件和子文件夹）
        if not os.path.exists(frame_path):  # 检查文件夹是否存在
            shot_count=0
        else:
            for item in os.listdir(frame_path):
                item_path = os.path.join(frame_path, item)
                if os.path.isfile(item_path):  # 检查是否为文件
                    shot_count += 1
        ASL = int(video.get(cv2.CAP_PROP_FRAME_COUNT) / shot_count) if shot_count != 0 else 0
        self.properties = [
            ('File', os.path.basename(filename)),
            ('FPS', video.get(cv2.CAP_PROP_FPS)),
            ('Width', int(video.get(cv2.CAP_PROP_FRAME_WIDTH))),
            ('Height', int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))),
            ('ASL', ASL),
            ('Frame count', int(video.get(cv2.CAP_PROP_FRAME_COUNT))),
            ('Shot count',shot_count)
        ]

        video.release()

        self.video_info_loaded.emit(self.properties)

    def update_table(self, properties):
        self.table.setRowCount(0)

        for i, (prop, value) in enumerate(properties):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(prop))
            self.table.setItem(i, 1, QTableWidgetItem(str(value)))
