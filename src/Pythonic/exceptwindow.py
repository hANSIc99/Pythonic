from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtCore import QCoreApplication as QC
import logging
from Pythonic.elementeditor import ElementEditor
from Pythonic.record_function import alphabet


class ExceptWindow(QWidget):

    window_closed = pyqtSignal(object, name='except_window_closed')

    def __init__(self, message, position):

        super().__init__()
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.Window)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.message = message
        self.position = position
        self.initUI()
        self.raiseWindow()

    def initUI(self):

        self.confirm_button = QPushButton()

        self.headline = QFont("Arial", 10, QFont.Bold)

        self.elementInfo = QLabel()
        self.elementInfo.setFont(self.headline)

        self.exceptionMessage = QTextEdit()
        self.exceptionMessage.setReadOnly(True)

        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.Window)

        self.exceptWindowLayout = QVBoxLayout()
        self.exceptWindowLayout.addWidget(self.elementInfo)
        self.exceptWindowLayout.addWidget(self.exceptionMessage)
        self.exceptWindowLayout.addStretch(1)
        self.exceptWindowLayout.addWidget(self.confirm_button)

        self.confirm_button.clicked.connect(self.close)

        self.setLayout(self.exceptWindowLayout)

    def raiseWindow(self):

        logging.debug('raiseWindow() called')

        self.confirm_button.setText(QC.translate('', 'Ok'))
        self.info_string = QC.translate('', 'Exception in element: ')
        self.elementInfo.setText(self.info_string + '{} {}'.format(self.position[0], alphabet[self.position[1]]))
        self.exceptionMessage.setText(self.message)
        self.setWindowTitle(QC.translate('', 'Exception found'))
        self.show()

    def closeEvent(self, event):
        logging.debug('closeEvent() called ExceptWindow')
        self.window_closed.emit(self.position)
        self.close()

