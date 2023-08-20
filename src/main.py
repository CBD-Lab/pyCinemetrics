import sys
import os
import importlib
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QAction, QMessageBox, QProgressBar
)
from PySide2.QtCore import Qt, Signal
from ui.vlcplayer import VLCPlayer
from ui.timeline import Timeline
import qdarktheme
from helper import resource_path


class MainWindow(QMainWindow):
    filename = Signal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.filename.connect(self.on_filename_changed)
        self.on_filename_changed()

        self.setWindowIcon(QIcon(resource_path('resources/icon.ico')))

        self.player = VLCPlayer(self)
        self.setCentralWidget(self.player)

        self.timeline = Timeline(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.timeline)

        self.info = QDockWidget('Info', self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.info)

        self.help = QDockWidget('Help', self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.help)

        self.control = QDockWidget('Control', self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.control)

        self.analyze = QDockWidget('Analyze', self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.analyze)

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
        about_action = QAction('&About', self)
        about_action.triggered.connect(
            lambda: QMessageBox.about(self, 'CCKS Cinemetrics', 'V0.1')
        )
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

        self.resizeDocks([self.info, self.help, self.control, self.analyze],
                         [int(self.width() * 0.3)] * 4, Qt.Horizontal)
        self.resizeDocks([self.timeline],
                         [int(self.height() * 0.5)], Qt.Vertical)

    def on_filename_changed(self, filename=None):
        if filename is None or filename == '':
            self.setWindowTitle('CCKS Cinemetrics')
        else:
            self.setWindowTitle('CCKS Cinemetrics - %s' % filename)


def main():
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    _ = MainWindow()

    if '_PYIBoot_SPLASH' in os.environ and \
            importlib.util.find_spec('pyi_splash'):
        import pyi_splash  # type: ignore
        pyi_splash.close()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
