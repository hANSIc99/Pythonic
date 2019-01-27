from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QStyleOption, QStyle,
                                QPushButton, QTextEdit, QMainWindow)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QPoint, QRect
from PyQt5.QtCore import QCoreApplication as QC
from PyQt5.QtCore import QThread
from elementmaster import alphabet
import multiprocessing as mp
from elementeditor import ElementEditor
import logging, sys, time, traceback


class DebugWindow(QWidget):

    proceed_execution = pyqtSignal(name='proceed_execution')

    def __init__(self, message, source):

        super().__init__()
    
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.source = source
        self.message = message

    def raiseWindow(self):

        logging.debug('raiseWindow() called')
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(QC.translate('', 'Debug'))
        self.setWindowModality(Qt.WindowModal)

        self.confirm_button = QPushButton()
        self.confirm_button.setText(QC.translate('', 'Ok'))
        self.confirm_button.clicked.connect(self.close)

        self.headline = QFont("Arial", 10, QFont.Bold)

        self.info_string = QC.translate('', 'Debug info of element:')
        self.elementInfo = QLabel()
        self.elementInfo.setFont(self.headline)
        self.elementInfo.setText(self.info_string + '{} {}'.format(self.source[0],
            alphabet[self.source[1]]))

        self.debugMessage = QTextEdit()
        self.debugMessage.setReadOnly(True)
        self.debugMessage.setText(self.message)



        self.debugWindowLayout = QVBoxLayout()
        self.debugWindowLayout.addWidget(self.elementInfo)
        self.debugWindowLayout.addWidget(self.debugMessage)
        self.debugWindowLayout.addStretch(1)
        self.debugWindowLayout.addWidget(self.confirm_button)

        self.setLayout(self.debugWindowLayout)   
        
        self.show()

    def closeEvent(self, event):
        logging.debug('closeEvent() called DebugWindow')
        self.proceed_execution.emit()
        self.hide()

