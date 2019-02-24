from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy,
        QStyleOption, QStyle, QPushButton, QTextEdit, QListWidgetItem, QListWidget)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont, QColor, QBrush
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QPoint, QRect
from PyQt5.QtCore import QCoreApplication as QC
from PyQt5.QtCore import QThread
from elementmaster import alphabet
import multiprocessing as mp
from elementeditor import ElementEditor
import logging, sys, time, traceback

class StackItem(QListWidgetItem):

    def __init__(self, parent, position):

        super().__init__(parent)
        self.parent = parent
        self.setAttribute(Qt,WA_DeleteOnClose, True)

        self.setText(position)

class StackWindow(QWidget):

    closed = pyqtSignal(name='StackWindow_closed')

    def __init__(self, parent):

        super().__init__(parent)
        self.parent = parent
        self.setAttribute(Qt.WA_DeleteOnClose, True)

    def raiseWindow(self):

        logging.debug('StackWindow() called')
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(QC.translate('', 'Stack'))
        #self.setWindowModality(Qt.WindowModal)

        self.confirm_button = QPushButton()
        self.confirm_button.setText(QC.translate('', 'Ok'))
        self.confirm_button.clicked.connect(self.close)

        self.headline = QFont("Arial", 10, QFont.Bold)

        self.info_string = QC.translate('', 'Debug info of element:')
        self.elementInfo = QLabel()
        self.elementInfo.setFont(self.headline)
        #self.elementInfo.setText(self.info_string + '{} {}'.format(self.source[0],
            #alphabet[self.source[1]]))
        self.elementInfo.setText('test 123')

        #QListWidgetItem = Stack Element

        self.stack_0 = QListWidgetItem()
        self.stack_0.setBackground(QBrush(QColor('red')))
        self.stack_0.setText('Stack 0')
        self.stack_0.setTextAlignment(Qt.AlignCenter)

        self.stack_1 = QListWidgetItem()
        self.stack_1.setBackground(QBrush(QColor('green')))
        self.stack_1.setText('Stack 1')

        self.stack_2 = QListWidgetItem()
        self.stack_2.setBackground(QBrush(QColor('yellow')))
        self.stack_2.setText('Stack 2')

        # Will contain the QListWidgetItems
        self.stackWidget = QListWidget()

        self.stackWidget.insertItem(0, self.stack_0)
        self.stackWidget.insertItem(0, self.stack_1)
        self.stackWidget.insertItem(0, self.stack_2)

        self.debugWindowLayout = QVBoxLayout()
        self.debugWindowLayout.addWidget(self.elementInfo)
        self.debugWindowLayout.addWidget(self.stackWidget)
        self.debugWindowLayout.addStretch(1)
        self.debugWindowLayout.addWidget(self.confirm_button)

        self.setLayout(self.debugWindowLayout)   
        
        self.show()

    def closeEvent(self, event):

        logging.debug("QStackWindow::closeEvent() called")
        self.closed.emit()

    def updateStack(self):

        logging.info('updateStack() called')
        tmp_text = self.debugMessage.toPlainText()
        tmp_text += ' a'
        self.debugMessage.setText(tmp_text)


