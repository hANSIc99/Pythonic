from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy,
        QStyleOption, QStyle, QPushButton, QTextEdit, QListWidgetItem, QListWidget)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont, QColor, QBrush
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QPoint, QRect
from PyQt5.QtCore import QCoreApplication as QC
from PyQt5.QtCore import QThread
from elementmaster import alphabet
import multiprocessing as mp
from elementeditor import ElementEditor
import logging, sys, time, traceback, pickle
from time import localtime, strftime

class StackItem(QListWidgetItem):

    def __init__(self, even, data, new):

        super().__init__()
        self.setTextAlignment(Qt.AlignCenter)
        self.setText(str(data))

        if even:
            self.setBackground(QBrush(QColor('lightgrey')))


class StackWindow(QWidget):

    closed = pyqtSignal(name='StackWindow_closed')

    def __init__(self, parent):

        super().__init__(parent)
        self.parent = parent
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.timestamp = strftime('%H:%M:%S', localtime())

    def raiseWindow(self, filename):

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
        self.elementInfo.setText('Last update: {}'.format(self.timestamp))

        # Will contain the QListWidgetItems
        self.stackWidget = QListWidget()
        #QListWidgetItem = Stack Element
        #test_list = list(range(30))

        try:
            with open(filename, 'rb') as stack_file:
                logging.info('file opened successful')
                stack = pickle.load(stack_file)
                if not isinstance(stack, list):
                    logging.error('StackWindow::raiseWindow() cannot iterate -  file is not a list - \
                            file is type: {}'.format(type(stack_file)))
                    self.closed.emit()
                    return
                for i in stack:
            
                    if i % 2 == 0: # even numbers
                        is_even = True
                        logging.info('List element even {}'.format(i))
                    else: # uneven number
                        is_even = False
                        logging.info('List element uneven {}'.format(i))

                    self.stackWidget.addItem(StackItem(is_even, i, True))

        except Exception as e:
            logging.error('StackWindow::raiseWindow() exception while opening file: {}'.format(e))
            self.closed.emit()
            return

        """
        for i in test_list:
            
            if i % 2 == 0: # even numbers
                is_even = True
                logging.info('List element even {}'.format(i))
            else: # uneven number
                is_even = False
                logging.info('List element uneven {}'.format(i))

            self.stackWidget.addItem(StackItem(is_even, i, True))
        """

               
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

    def updateStack(self, filename):

        # list neu einlesen

        logging.info('StackWindow::updateStack() called with filename: {}'.format(
            filename))
        self.timestamp = strftime('%H:%M:%S', localtime())
        self.elementInfo.setText('Last update: {}'.format(self.timestamp))


