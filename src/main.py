import sys
# from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QAction, QMessageBox, QProgressBar
)
from PySide2.QtCore import Qt, Signal
from ui.timeline import Timeline
from ui.info import Info
from ui.analyze import Analyze
from ui.subtitle import Subtitle
import qdarktheme
from concurrent.futures import ThreadPoolExecutor
from helper import Splash
from ui.vlcplayer import VLCPlayer
from ui.control import Control


# from ui.subtitleEasyOcr import getsubtitleEasyOcr,subtitle2Srt

class MainWindow(QMainWindow):
    filename_changed = Signal(str)
    shot_finished = Signal()
    video_play_changed= Signal(int)

    def __init__(self):
        super().__init__()
        self.threadpool = ThreadPoolExecutor()
        self.filename = ''

        self.AnalyzeImgPath=''
        self.init_ui()

    def init_ui(self):
        #self.setWindowIcon(QIcon(resource_path('resources/icon.ico')))

        # Delay VLC import to here
        self.player = VLCPlayer(self)
        self.setCentralWidget(self.player)

        self.info = Info(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.info)

        self.subtitle = Subtitle(self,self.filename)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.subtitle)

        self.control = Control(self,self.filename)
        self.addDockWidget(Qt.RightDockWidgetArea, self.control)

        self.analyze = Analyze(self,self.filename)
        self.addDockWidget(Qt.RightDockWidgetArea, self.analyze)

        self.timeline = Timeline(self,self.control.colorsC)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.timeline)


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
        # self.subtitle.setFixedHeight(int(self.height() * 0.15))
        # self.analyze.setFixedHeight(int(self.height()*0.15))
        self.filename_changed.connect(self.on_filename_changed)
        self.on_filename_changed()
        self.video_play_changed.connect(self.player.on_video_play_changed)

    def on_filename_changed(self, filename=None):
        # self.labelAnalyze.setPixmap(QPixmap())
        if filename is None or filename == '':
            self.setWindowTitle('CCKS Cinemetrics')
        else:
            self.setWindowTitle('CCKS Cinemetrics - %s' % filename)
            self.filename = filename


def main():
    splash = Splash()
    splash.update('Loading VLC')
    # import vlc  # noqa

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
