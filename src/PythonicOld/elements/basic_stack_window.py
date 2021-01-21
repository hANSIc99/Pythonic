from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QListWidgetItem, QListWidget
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtCore import QCoreApplication as QC
import logging, pickle
from time import localtime, strftime
from Pythonic.elementeditor import ElementEditor
from Pythonic.record_function import alphabet

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
        self.elementInfoText = QC.translate('', 'Last update:')
        self.elementInfoText += ' {}'.format(self.timestamp)
        self.elementInfo.setText(self.elementInfoText)

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

        try:
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
                    self.seperatorwidgettext = QC.translate('', 'Element')
                    self.seperatorwidgettext += ' 21 - {} '.format(str(len(stack)-20))
                    self.seperatorwidgettext += QC.translate('', 'hidden')
                    self.seperator_widget.setText(self.seperatorwidgettext)
                    self.seperator_widget.setBackground(QBrush(QColor('#CCCC00')))
                    self.stackWidget.addItem(self.seperator_widget)


                    for i in range(len(stack)-20, len(stack)):
                        if i % 2 == 0: # even numbers
                            is_even = True
                        else: # uneven number
                            is_even = False

                        self.stackWidget.addItem(StackItem(is_even, stack[i], True))
        except Exception as e:
            logging.error('StackWindow::restock() exception while opening file: {}'.format(e))

        
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


