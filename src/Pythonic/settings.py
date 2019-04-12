from PyQt5.QtWidgets import (QWidget,
                            QApplication,
                            QFrame, QPushButton, QTextEdit,
                            QHBoxLayout, QAction, QMainWindow, QLineEdit,
                            QVBoxLayout, QSizePolicy, QMenu, QMessageBox,
                            QGridLayout, QSizeGrip, QTabWidget, QMenuBar,
                            QLabel, QScrollArea, QGraphicsView, QGraphicsScene)
from PyQt5.QtCore import (Qt, QMimeData, QByteArray, QDataStream, QPoint, QLocale,
                         QThreadPool, QDir, pyqtSignal, pyqtSlot, QRect, QTranslator, QEvent)
from PyQt5.QtGui import (QDrag, QPixmap, QPainter,QColor,
                        QScreen, QPainter, QFont, QIntValidator)

from PyQt5.QtCore import QCoreApplication as QC
import sys, logging
from Pythonic.elementeditor import ElementEditor

class Settings(QWidget):

    def __init__(self):

        logging.debug('__init__() called SettingsWindow')
        super().__init__()

        self.delay = 500

    def show(self):

        logging.debug('edit() called ExecReturn')
        self.settingsLayout = QVBoxLayout()
        self.delayRow = QWidget()
        self.delayRowLayout = QHBoxLayout()

        self.window = ElementEditor(self)
        self.window.setWindowTitle(QC.translate('', 'Settings'))

        self.top_text = QLabel()
        self.top_text.setText(QC.translate('', 'Debug delay:'))

        self.delay_text = QLabel()
        self.delay_text.setText(QC.translate('', 'Milliseconds'))

        self.delayInput = QLineEdit()
        self.delayInput.setValidator(QIntValidator(0, 9999))
        self.delayInput.setText(str(self.delay))

        self.delayRowLayout.addWidget(self.delayInput)
        self.delayRowLayout.addWidget(self.delay_text)
        self.delayRowLayout.addStretch(1)

        self.delayRow.setLayout(self.delayRowLayout)

        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.confirm_button.clicked.connect(self.window.closeEvent)
        self.window.window_closed.connect(self.edit_done)

        self.settingsLayout.addWidget(self.top_text)
        self.settingsLayout.addWidget(self.delayRow)
        self.settingsLayout.addStretch(1)
        self.settingsLayout.addWidget(self.confirm_button)
        self.window.setLayout(self.settingsLayout)
        self.window.show()


    def edit_done(self):
        logging.debug('edit_done() called : delay {} MS'.format(self.delayInput.text()))
        self.delay = int(self.delayInput.text())

