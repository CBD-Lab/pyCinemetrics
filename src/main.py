import sys
import os
import importlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget
from PyQt5.QtCore import Qt
import qdarktheme


class HelloWorld(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        from vlcplayer import VLCPlayer
        widget = VLCPlayer(self)
        self.setCentralWidget(widget)
        self.setWindowTitle('CCKS Cinemetrics')

        self.timeline = QDockWidget("Timeline", self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.timeline)

        self.info = QDockWidget("Info", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.info)

        self.help = QDockWidget("Help", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.help)

        self.control = QDockWidget("Control", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.control)

        self.analyze = QDockWidget("Analyze", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.analyze)

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

        self.resizeDocks([self.info, self.help, self.control, self.analyze],
                         [int(self.width() * 0.3)] * 4, Qt.Horizontal)
        self.resizeDocks([self.timeline],
                         [int(self.height() * 0.5)], Qt.Vertical)


def main():
    if '_PYIBoot_SPLASH' in os.environ and \
            importlib.util.find_spec("pyi_splash"):
        import pyi_splash  # type: ignore
        pyi_splash.close()

    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    _ = HelloWorld()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
