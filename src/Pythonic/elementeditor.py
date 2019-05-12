from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget
import logging

class ElementEditor(QWidget):

    window_closed = pyqtSignal(name='window_closed')

    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.Window)
        self.setWindowModality(Qt.WindowModal)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        logging.debug('ElementEditor::__init__() called')

    def closeEvent(self, event):
        logging.debug('ElementEditor::closeEvent() called')
        self.window_closed.emit()
        self.hide()

