from PySide2.QtWidgets import QDockWidget


class Timeline(QDockWidget):
    def __init__(self, parent):
        super().__init__('Timeline', parent)
        self.init_ui()

    def init_ui(self):
        pass
