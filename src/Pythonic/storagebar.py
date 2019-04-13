from PyQt5.QtWidgets import (QWidget,
                            QApplication,
                            QFrame, QPushButton, QTextEdit,
                            QHBoxLayout, QAction, QMainWindow,
                            QVBoxLayout, QSizePolicy, QMenu, QMessageBox,
                            QGridLayout, QSizeGrip, QTabWidget, QMenuBar,
                            QLabel, QScrollArea, QGraphicsView, QGraphicsScene)
from PyQt5.QtCore import (Qt, QMimeData, QByteArray, QDataStream, QPoint, QLocale,
                         QThreadPool, QDir, pyqtSignal, pyqtSlot, QRect, QTranslator, QEvent)
from PyQt5.QtGui import (QDrag, QPixmap, QPainter,QColor,
                        QScreen, QPainter, QFont)

from PyQt5.QtCore import QCoreApplication as QC
from dropbox import DropBox
import sys, logging

class StorageBar(QWidget):

    load_config = pyqtSignal(int, int, object, name='load_config')

    def __init__(self):

        super().__init__()
        self.setMinimumWidth(200)
        self.box_frame = QVBoxLayout()
        self.box_frame.setContentsMargins(0, 0, 0, 0)
        self.icon_bar = QWidget()
        self.icon_bar_spacer = QWidget()
        self.icon_bar.setStyleSheet('background-color: rgba(77, 103, 125, 0.5);\
                border-radius: 10px')
        #self.icon_bar.setStyleSheet('background-color: \
        #        qlineargradient(x1:0.5 y1:0, x2:0.5 y2:1, stop:0 #646464, stop:1 #366a97);\
        #        border-radius: 10px')


        policy = QSizePolicy()
        policy.setRetainSizeWhenHidden(True)

        self.icon_bar.setSizePolicy(policy)


        # widget which contains the icons
        self.iconBox = QVBoxLayout()
        self.iconBox_spacer = QVBoxLayout()

        self.iconBox_spacer.addStretch(1)

        self.iconBox.setContentsMargins(0, 0, 0, 0)
        self.iconBox_spacer.setContentsMargins(0, 0, 0, 0)

        self.icon_bar.setLayout(self.iconBox)
        self.icon_bar_spacer.setLayout(self.iconBox_spacer)

        self.box_frame.addWidget(self.icon_bar)
        self.box_frame.addWidget(self.icon_bar_spacer)

        self.setLayout(self.box_frame) 
        self.addBox()

        self.tmp_config = None
        self.tmp_element = None

    def addBox(self):
        
        new_box = DropBox(self)
        new_box.drop_storage.connect(self.storeSignal)

        self.iconBox.addWidget(new_box)

    def storeSignal(self, row, column):

        logging.debug('StorageBar::storeSignal() called - delete row {} - column {}'.format(
            row, column))
        self.addBox()

        element = self.parent().grid.itemAtPosition(row, column).widget()
        # parent() to access the grid
        self.parent().delete_element(row, column)


    def checkStore(self, row, column):

        element = self.parent().grid.itemAtPosition(row, column).widget()

        return self.parent().checkDeletion(element)

    def saveConfig(self, row, column):

        logging.debug('StorageBar::saveConfig() called')

        element = self.parent().grid.itemAtPosition(row, column).widget()
        return element.config

    def returnConfig(self):

        logging.debug('StorageBar::returnConfig() called')
        self.tmp_element.destroy()
        return self.tmp_config
    

