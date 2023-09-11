from PySide2.QtWidgets import (
    QDockWidget, QTextEdit
)


class Subtitle(QDockWidget):
    def __init__(self, parent,filename):
        super().__init__('Subtitle', parent)
        self.parent = parent
        self.filename=filename
        self.parent.filename_changed.connect(self.on_filename_changed)
        self.init_subtitle()
    def init_subtitle(self):
        self.textSubtitle = QTextEdit(
            "Subtitle…… ", self)
        self.textSubtitle.setGeometry(10,30, 300, 300)

    def on_filename_changed(self,filename):
        self.filename=filename
        self.textSubtitle.setPlainText("Subtitle…… ")
