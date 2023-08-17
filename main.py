import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDockWidget
from PyQt5.QtCore import Qt
from player import Player


class HelloWorld(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        widget = Player(self)
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

        print(self.size().width())
        print(self.size().height())

        self.resizeDocks([self.info, self.help, self.control, self.analyze],
                        [int(self.width() * 0.2)] * 4, Qt.Horizontal)
        self.resizeDocks([self.timeline], [int(self.height() * 0.2)], Qt.Vertical)


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = HelloWorld()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
