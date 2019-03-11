from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy,
        QStyleOption, QStyle, QPushButton, QTextEdit, QListWidgetItem, QListWidget,
        QSizePolicy)
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

        self.confirm_button = QPushButton()
        self.confirm_button.setText(QC.translate('', 'Ok'))
        self.confirm_button.clicked.connect(self.close)

        self.headline = QFont("Arial", 10, QFont.Bold)

        self.info_string = QC.translate('', 'Debug info of element:')
        self.elementInfo = QLabel()
        self.elementInfo.setFont(self.headline)
        self.elementInfo.setText('Last update: {}'.format(self.timestamp))

        # Will contain the QListWidgetItems
        self.stackWidget = QListWidget()

        try:
            self.restock(filename)
        except Exception as e:
            logging.error('StackWindow::raiseWindow() exception while opening file: {}'.format(e))
            self.closed.emit()
            return

               
        self.debugWindowLayout = QVBoxLayout()
        self.debugWindowLayout.addWidget(self.elementInfo)
        self.debugWindowLayout.addWidget(self.stackWidget)
        self.debugWindowLayout.addWidget(self.confirm_button)

        self.setLayout(self.debugWindowLayout)   
        
        self.show()

    def restock(self, filename):

        logging.debug('StackWindow::restock() called with filename: {}'.format(
            filename))
        if self.stackWidget.item(0) != None:
            while self.stackWidget.count() != 0:
                self.stackWidget.takeItem(0)

        with open(filename, 'rb') as stack_file:
            stack = pickle.load(stack_file)
            if not isinstance(stack, list):
                logging.error('StackWindow::raiseWindow() cannot iterate - \
                        file is not a list - \
                        file is type: {}'.format(type(stack_file)))
                self.closed.emit()
                return

            if len(stack) <= 40:
                for i, data in enumerate(stack):
    
                    if i % 2 == 0: # even numbers
                        is_even = True
                    else: # uneven number
                        is_even = False

                    self.stackWidget.addItem(StackItem(is_even, data, True))
            else:
                for i in range(20): #print element 0 - 19
                    if i % 2 == 0: # even numbers
                        is_even = True
                    else: # uneven number
                        is_even = False

                    self.stackWidget.addItem(StackItem(is_even, stack[i], True))
                # seperator element when the list is long
                self.seperator_widget = QListWidgetItem()
                self.seperator_widget.setTextAlignment(Qt.AlignCenter)
                self.seperator_widget.setText("Element 21 - {} hidden".format(
                    str(len(stack)-20)))
                self.seperator_widget.setBackground(QBrush(QColor('#CCCC00')))
                self.stackWidget.addItem(self.seperator_widget)


                for i in range(len(stack)-20, len(stack)):
                    if i % 2 == 0: # even numbers
                        is_even = True
                    else: # uneven number
                        is_even = False

                    self.stackWidget.addItem(StackItem(is_even, stack[i], True))

        
    def closeEvent(self, event):

        logging.debug("QStackWindow::closeEvent() called")
        self.closed.emit()

    def updateStack(self, filename):

        logging.debug('StackWindow::updateStack() called with filename: {}'.format(
            filename))
        self.timestamp = strftime('%H:%M:%S', localtime())
        self.elementInfo.setText('Last update: {}'.format(self.timestamp))
        self.restock(filename)
        self.stackWidget.update()


