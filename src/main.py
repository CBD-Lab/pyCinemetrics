import sys
import os
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QAction, QMessageBox, QProgressBar,
    QPushButton, QLabel,QSlider
)
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QPixmap

from ui.timeline import Timeline
from ui.info import Info
import qdarktheme
from concurrent.futures import ThreadPoolExecutor
from helper import resource_path, Splash

from ui.shotcut import findshot, imgColors
from algorithms.VGG19CpuGpu import objectDetection
from shots.subtitleEasyOcr import getsubtitleEasyOcr,subtitle2Srt


class MainWindow(QMainWindow):
    filename_changed = Signal(str)
    shot_finished = Signal()
    video_play_changed= Signal(int)

    def __init__(self):
        super().__init__()
        self.threadpool = ThreadPoolExecutor()
        self.init_ui()
        self.filename = ''
        #self.frameId=''

    def init_ui(self):
        self.filename_changed.connect(self.on_filename_changed)
        self.on_filename_changed()


        #self.setWindowIcon(QIcon(resource_path('resources/icon.ico')))

        # Delay VLC import to here
        from ui.vlcplayer import VLCPlayer
        self.player = VLCPlayer(self)
        self.setCentralWidget(self.player)

        self.timeline = Timeline(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.timeline)

        self.info = Info(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.info)

        self.subtitle = QDockWidget('Subtitle', self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.subtitle)

        self.control = QDockWidget('Control', self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.control)

        self.analyze = QDockWidget('Analyze', self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.analyze)

        self.shots= QPushButton("ShotCut", self.control)
        self.shots.setGeometry(2, 30, 100, 30)
        self.shots.clicked.connect(self.shotcut)

        self.colors = QPushButton("Colors", self.control)
        self.colors.setGeometry(2, 65, 100, 30)
        self.colors.clicked.connect(self.colorAnalyze)

        self.objects = QPushButton("Objects", self.control)
        self.objects.setGeometry(2, 100, 100, 30)
        self.objects.clicked.connect(self.objectDetectionVgg19)

        self.subtitleBtn = QPushButton("Subtitles", self.control)
        self.subtitleBtn.setGeometry(2, 135, 100, 30)
        self.subtitleBtn.clicked.connect(self.getsubtitles)

        self.thSlider = QSlider(Qt.Horizontal,self.control) # 水平方向
        self.thSlider.setGeometry(140, 30, 100, 30)
        self.thSlider.setMinimum(20)  # 设置最小值
        self.thSlider.setMaximum(100)  # 设置最大值
        self.thSlider.setSingleStep(1)  # 设置步长值
        self.thSlider.setValue(35)  # 设置当前值
        self.thSlider.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.thSlider.setTickInterval(10)  # 设置刻度间隔
        self.thSlider.valueChanged.connect(self.thSliderChange)

        self.colorsCategory = QSlider(Qt.Horizontal,self.control) # 水平方向
        self.colorsCategory.setGeometry(140, 65, 100, 30)
        self.colorsCategory.setMinimum(3)  # 设置最小值
        self.colorsCategory.setMaximum(20)  # 设置最大值
        self.colorsCategory.setSingleStep(1)  # 设置步长值
        self.colorsCategory.setValue(5)  # 设置当前值
        self.colorsCategory.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.colorsCategory.setTickInterval(5)  # 设置刻度间隔
        self.colorsCategory.valueChanged.connect(self.colorChange)

        self.labelThSlider = QLabel(
            "0.35", self.control)
        self.labelThSlider.setGeometry(250, 30, 100, 40)

        self.labelColors = QLabel(
            "5", self.control)
        self.labelColors.setGeometry(250, 65, 100, 40)


        self.labelSubtitle = QLabel(
            "Subtitle…… ", self.subtitle)
        self.labelSubtitle.setGeometry(2, 30, 100, 40)

        self.labelAnalyze = QLabel("", self.analyze)
        self.labelAnalyze.setGeometry(2, 30, 300, 300)

        menu = self.menuBar()

        file_menu = menu.addMenu('&File')
        open_action = QAction('&Open', self)
        open_action.triggered.connect(lambda: self.player.open_file())
        exit_action = QAction('&Exit', self)
        exit_action.triggered.connect(lambda: self.close())
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        help_menu = menu.addMenu('&Help')
        manual_action = QAction('&Manual', self)
        manual_action.triggered.connect(
            lambda: QMessageBox.about(self, ' CCKS Cinemetrics V0.1',' 1-Open Video Play(VLC)\n 2-ShotCut(aHash)\n 3-Color Analyze(Kmeans)\n 4-Subtitle(OCR)\n 5-Object Detection(VGG19)\n 6-Field of view(OpenPose)\n')
        )

        about_action = QAction('&About', self)
        about_action.triggered.connect(
            lambda: QMessageBox.about(self, 'CCKS Cinemetrics', 'CCKS Cinemetrics V0.1 \nHttp://movie.yingshinet.com')
        )
        help_menu.addAction(manual_action)
        help_menu.addAction(about_action)

        status_bar = self.statusBar()
        self.progressBar = QProgressBar()
        status_bar.showMessage('')
        status_bar.addPermanentWidget(self.progressBar)
        self.progressBar.hide()

        app = QApplication.instance()
        screen = app.primaryScreen()
        geometry = screen.availableGeometry()
        self.setGeometry(
            int(geometry.width() * 0.1),
            int(geometry.height() * 0.1),
            int(geometry.width() * 0.8),
            int(geometry.height() * 0.8)
        )
        self.showMaximized()

        self.resizeDocks([self.info, self.subtitle, self.control, self.analyze],
                         [int(self.width() * 0.3)] * 4, Qt.Horizontal)
        self.resizeDocks([self.timeline],
                         [int(self.height() * 0.5)], Qt.Vertical)

    def on_filename_changed(self, filename=None):
        if filename is None or filename == '':
            self.setWindowTitle('CCKS Cinemetrics')
        else:
            self.setWindowTitle('CCKS Cinemetrics - %s' % filename)
            self.filename = filename

    def thSliderChange(self):
        print("current slider value:"+str(self.thSlider.value()))
        self.th= self.thSlider.value()/100
        self.labelThSlider.setText(str(self.th))

    def colorChange(self):
        print("current Color Category slider value:"+str(self.thSlider.value()))
        self.colorsC= self.colorsCategory.value()
        self.labelColors.setText(str(self.colorsC))

    def shotcut(self):

        #self.th = 0.35
        # self.v_path='./video/20210701.mp4'
        # self.image_save="./img/20210701"
        self.v_path = self.filename
        print(self.v_path)
        # imgpath = os.path.basename(self.v_path)[0:-4]
        self.image_save = "./img/"+str(os.path.basename(self.v_path)[0:-4])
        print(self.image_save)
        findshot(self.v_path, self.image_save, self.th)
        self.shot_finished.emit()

        self.shotdiff = QPixmap(self.image_save+".png")
        self.shotdiff = self.shotdiff.scaled(
            self.analyze.width(), self.analyze.width())
        self.labelAnalyze.setPixmap(self.shotdiff)


    def colorAnalyze(self):
        imgpath = os.path.basename(self.filename)[0:-4]
        print(imgpath)
        imgColors(imgpath,self.colorsC)

    def objectDetectionVgg19(self):
        imgpath = os.path.basename(self.filename)[0:-4]
        print(imgpath)
        k=objectDetection(r"./img/"+imgpath+"/")


    def getsubtitles(self,filename):
        print(self.filename)
        subtitleStr,subtitleList=getsubtitleEasyOcr(self.filename)
        imgpath = os.path.basename(self.filename)[0:-4]
        print(imgpath)
        save_path=r"./img/" + imgpath + "/"
        subtitle2Srt(subtitleList,save_path)
        self.labelSubtitle.setText(subtitleStr)
def main():
    splash = Splash()
    splash.update('Loading VLC')
    import vlc  # noqa

    splash.update('Initialize QT')
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    splash.update('Initialize GUI')
    _ = MainWindow()

    splash.close()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
