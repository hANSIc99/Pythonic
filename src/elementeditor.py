from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QTextEdit, QWidget,
        QComboBox, QCheckBox, QGridLayout, QSpacerItem, QLineEdit, QPushButton)
from PyQt5.QtCore import QCoreApplication as QC
import logging
from time import sleep

class ElementEditor(QWidget):

    window_closed = pyqtSignal(name='window_closed')

    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.Window)
        self.setWindowModality(Qt.WindowModal)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        logging.debug('__init__() called ElementEditor')

    def closeEvent(self, event):
        logging.debug('closeEvent() called ElementEditor')
        self.window_closed.emit()
        self.hide()

