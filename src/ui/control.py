import functools

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (
    QDockWidget, QPushButton, QLabel, QFileDialog, QSlider, QMessageBox, QVBoxLayout,
    QWidget, QGridLayout
)
from PySide2.QtCore import Qt
from src.algorithms.objectDetection import ObjectDetection
from src.algorithms.resultsave import resultsave
from src.algorithms.shotscale import shotscale
from src.algorithms.subtitleEasyOcr import *
from src.algorithms.shotcutTransNetV2 import transNetV2_run
from src.algorithms.subtitleEasyOcr import SubtitleProcessor
from src.algorithms.img2Colors import ColorAnalysis

class Control(QDockWidget):
    def __init__(self, parent,filename):
        super().__init__('Control', parent)
        self.parent = parent
        self.filename=filename
        self.AnalyzeImg=""
        self.AnalyzeImgPath=""
        self.parent.filename_changed.connect(self.on_filename_changed)
        # self.video_info_loaded.connect(self.update_table)
        self.th = 0.35
        self.colorsC = 5
        self.subtitleValue = 48
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        self.shotcut = QPushButton("ShotCut", self)
        self.shotcut.clicked.connect(self.shotcut_transNetV2)

        self.colors = QPushButton("Colors", self)
        self.colors.clicked.connect(self.colorAnalyze)

        self.objects = QPushButton("Objects", self)
        self.objects.clicked.connect(self.object_detect)

        self.subtitleBtn = QPushButton("Subtitles", self)
        self.subtitleBtn.clicked.connect(self.getsubtitles)

        self.shotscale = QPushButton("ShotScale", self)
        self.shotscale.clicked.connect(self.getshotscale)

        self.colorsSlider = QSlider(Qt.Horizontal, self)  # 水平方向
        self.colorsSlider.setMinimum(3)  # 设置最小值
        self.colorsSlider.setMaximum(20)  # 设置最大值
        self.colorsSlider.setSingleStep(1)  # 设置步长值
        self.colorsSlider.setValue(5)  # 设置当前值
        self.colorsSlider.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.colorsSlider.setTickInterval(5)  # 设置刻度间隔
        self.colorsSlider.valueChanged.connect(self.colorChange)

        self.subtitleSlider = QSlider(Qt.Horizontal, self)  # 水平方向
        self.subtitleSlider.setMinimum(12)  # 设置最小值
        self.subtitleSlider.setMaximum(120)  # 设置最大值
        self.subtitleSlider.setSingleStep(1)  # 设置步长值
        self.subtitleSlider.setValue(48)  # 设置当前值
        self.subtitleSlider.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.subtitleSlider.setTickInterval(5)  # 设置刻度间隔
        self.subtitleSlider.valueChanged.connect(self.subtitleChange)

        # self.labelThSlider = QLabel(
        #     "0.35", self.control)
        # self.labelThSlider.setGeometry(250, 30, 100, 40)

        self.labelColors = QLabel(
            "5", self)
        self.labelSubtitlevalue = QLabel("48", self)


        # shotcut下载按钮
        self.download_shotcut_button = QPushButton(".csv", self)
        self.download_shotcut_button.clicked.connect(
            functools.partial(self.show_save_dialog, "shotlen.csv")
        )

        self.download_color_button = QPushButton(".csv", self)
        self.download_shotcut_button.clicked.connect(
            functools.partial(self.show_save_dialog, "colors.csv")
        )

        self.download_object_button = QPushButton(".csv", self)
        self.download_object_button.clicked.connect(
            functools.partial(self.show_save_dialog, "objects.csv")
        )

        self.download_subtitle_button = QPushButton(".csv", self)
        self.download_subtitle_button.clicked.connect(
            functools.partial(self.show_save_dialog, "subtitle.csv")
        )

        self.download_shotscale_button = QPushButton(".csv", self)
        self.download_shotscale_button.clicked.connect(
            functools.partial(self.show_save_dialog, "shotscale.csv")
        )

        # 创建一个网格布局，并将进度条和标签添加到网格中
        grid_layout.addWidget(self.shotcut,0,0)
        grid_layout.addWidget(self.colors,1,0)
        grid_layout.addWidget(self.objects,2,0)
        grid_layout.addWidget(self.subtitleBtn,3,0)
        grid_layout.addWidget(self.shotscale,4,0)

        grid_layout.addWidget(self.colorsSlider, 1, 1)  # 第一行，第二列
        grid_layout.addWidget(self.labelColors, 1, 2)  # 第一行，第三列
        grid_layout.addWidget(self.subtitleSlider, 3, 1)  # 第二行，第二列
        grid_layout.addWidget(self.labelSubtitlevalue, 3, 2)  # 第二行，第三列

        grid_layout.addWidget(self.download_shotcut_button,0,3)
        grid_layout.addWidget(self.download_color_button,1,3)
        grid_layout.addWidget(self.download_object_button,2,3)
        grid_layout.addWidget(self.download_subtitle_button,3,3)
        grid_layout.addWidget(self.download_shotscale_button,4,3)

        # 创建一个QWidget，将主布局设置为这个QWidget的布局
        widget = QWidget()
        widget.setLayout(grid_layout)
        self.setWidget(widget)
    def on_filename_changed(self,filename):
        self.filename=filename
    def shotcut_transNetV2(self):
        self.v_path = self.filename  # 视频路径
        self.frame_save = "./img/" + str(os.path.basename(self.v_path)[0:-4]) + "/frame"  # 图片存储路径
        self.image_save = "./img/" + str(os.path.basename(self.v_path)[0:-4])
        shot_len = transNetV2_run(self.v_path, self.image_save, self.th)
        rs=resultsave(self.image_save+"/")
        rs.plot_transnet_shotcut(shot_len)
        rs.diff_csv(0, shot_len)
        self.parent.shot_finished.emit()

        self.AnalyzeImg = QPixmap(self.image_save + "/shotlen.png")
        self.AnalyzeImgPath = self.image_save + "/shotlen.png"
        self.AnalyzeImg = self.AnalyzeImg.scaled(
            250, 160)
        self.parent.analyze.labelAnalyze.setPixmap(self.AnalyzeImg)
        # self.toggle_button.setVisible(False)

    def colorAnalyze(self):
        imgpath = os.path.basename(self.filename)[0:-4]
        coloranalysis=ColorAnalysis("")
        coloranalysis.imgColors(imgpath, self.colorsC)

        self.AnalyzeImg = QPixmap("img/" + imgpath + "/" + "colors.png")
        self.AnalyzeImgPath = "img/" + imgpath + "/" + "colors.png"
        self.AnalyzeImg = self.AnalyzeImg.scaled(
            250, 160)
        self.parent.analyze.labelAnalyze.setPixmap(self.AnalyzeImg)

        # self.toggle_button.setVisible(False)  # 初始时不显示按钮

    def object_detect(self):
        imgpath = os.path.basename(self.filename)[0:-4]
        objectdetection=ObjectDetection(r"./img/" + imgpath)
        self.AnalyzeImg = QPixmap("img/" + imgpath + "/objects.png")
        self.AnalyzeImgPath = "img/" + imgpath + "/objects.png"
        self.AnalyzeImg = self.AnalyzeImg.scaled(
            250, 160)
        # print(self.AnalyzeImgPath)
        k = objectdetection.object_detection()
        self.parent.analyze.labelAnalyze.setPixmap(self.AnalyzeImg)
        # self.toggle_button.setVisible(False)  # 初始时不显示按钮

    def getsubtitles(self, filename):
        imgpath = os.path.basename(self.filename)[0:-4]
        save_path = r"./img/" + imgpath + "/"
        subtitleprocesser=SubtitleProcessor()
        subtitleStr, subtitleList = subtitleprocesser.getsubtitleEasyOcr(self.filename, save_path, self.subtitleValue)
        # print("显示字幕结果", subtitleStr)
        subtitleprocesser.subtitle2Srt(subtitleList, save_path)
        self.parent.subtitle.textSubtitle.setPlainText(subtitleStr)

        self.v_path = self.filename  # 视频路径
        self.parent.shot_finished.emit()

        self.AnalyzeImg = QPixmap("img/" + imgpath + "/" + "subtitle.png")
        self.AnalyzeImgPath = "img/" + imgpath + "/" + "subtitle.png"
        self.AnalyzeImg = self.AnalyzeImg.scaled(
            250, 160)
        self.parent.analyze.labelAnalyze.setPixmap(self.AnalyzeImg)

        # self.toggle_button.setVisible(False)  # 初始时不显示按钮

    def getshotscale(self):
        image_save = "./img/" + str(os.path.basename(self.filename)[0:-4]) + "/"
        self.frame_save = "./img/" + str(os.path.basename(self.filename)[0:-4]) + "/frame/"  # 图片存储路径
        ss = shotscale(25)

        csv_file = image_save + "shotscale.csv"
        if not os.path.exists(csv_file):
            image_files = [f for f in os.listdir(self.frame_save) if f.endswith((".jpg", ".jpeg", ".png"))]
            print(self.frame_save)
            result = []
            for img in image_files:
                print(img)
                imgDetect, type, num = ss.predict(self.frame_save + img)
                # cv2.imshow("frame", imgDetect)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                print("Detected People:", num)
                frame_id = img.replace("frame", "").replace(".jpg", "").replace(".jpeg", "").replace(".png", "")
                result.append([frame_id, type, num])
            ss.shotscale_csv(result, image_save)

        png_file = image_save + "shotscale.png"
        if os.path.exists(png_file):
            self.AnalyzeImgPath = png_file
        else:
            ss.shotscale_plot(result, image_save)
            self.AnalyzeImgPath = image_save + "shotscale.png"
        self.AnalyzeImg = QPixmap(self.AnalyzeImgPath)
        self.AnalyzeImg = self.AnalyzeImg.scaled(250, 160)
        self.parent.analyze.labelAnalyze.setPixmap(self.AnalyzeImg)

        # self.toggle_button.setVisible(False)  # 初始时不显示按钮

    def show_save_dialog(self, file_name):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", "", options=options
        )

        if directory:
            self.download_resources(directory, file_name)

    # def thSliderChange(self):
    #     print("current slider value:"+str(self.thSlider.value()))
    #     self.th= self.thSlider.value()/100
    #     self.labelThSlider.setText(str(self.th))

    def show_save_dialog(self, file_name):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", "", options=options
        )

        if directory:
            self.download_resources(directory, file_name)
    # def thSliderChange(self):
    #     print("current slider value:"+str(self.thSlider.value()))
    #     self.th= self.thSlider.value()/100
    #     self.labelThSlider.setText(str(self.th))

    def colorChange(self):
        print("current Color Category slider value:"+str(self.colorsSlider.value()))
        self.colorsC= self.colorsSlider.value()
        self.labelColors.setText(str(self.colorsC))
    def subtitleChange(self):
        print("current subtitle Category slider value:" + str(self.subtitleSlider.value()))
        self.subtitleValue = self.subtitleSlider.value()
        self.labelSubtitlevalue.setText(str(self.subtitleValue))
    def download_resources(self,directory,file_name):
        # 在这里编写复制资源的代码
        # 你需要将指定的资源文件复制到用户选择的 save_path
        # 例如：
        import shutil
        imgpath = os.path.basename(self.filename)[0:-4]
        resource_path ='./img/'+imgpath+"/"+file_name
        destination_path = os.path.join(directory, file_name)
        shutil.copy(resource_path, destination_path)

        QMessageBox.information(self, "Download", "Resource downloaded successfully!")