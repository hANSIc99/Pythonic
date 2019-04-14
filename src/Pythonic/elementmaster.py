from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout,
        QSizePolicy, QStyleOption, QStyle, QPushButton, QTextEdit, QMainWindow)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont, QDrag, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect, QMimeData
from PyQt5.QtCore import QCoreApplication as QC
from element_iconbar import IconBar
from elementeditor import ElementEditor
from time import sleep
import logging, sys, traceback
from Pythonic.record_function import Function


alphabet = { 0 : 'A', 1 : 'B', 2 : 'C', 3 : 'D', 4 : 'E', 5 : 'F', 6 : 'G', 7 : 'H', 8 : 'J',
        9 : 'K', 10 : 'L', 11 : 'M', 12 : 'N', 13 : 'O', 14 : 'P', 15 : 'Q', 16 : 'R', 17 : 'S',
        18 : 'T', 19 : 'U', 20 : 'V', 21 : 'W', 22 : 'X', 23 : 'Y', 24 : 'Z'}

class ElementMaster(QWidget):


    del_sig = pyqtSignal(int, int, name='delete_element')
    edit_sig = pyqtSignal(name='edit_element')
    #function position updaten wenn eigene position verschoben wird

    def __init__(self, row, column, pixmap, state_iconBar, config, self_sync=False):

        logging.debug('ElementMaster::__init__() called {}'.format((self.row, self.column)))
        super().__init__()
        self.row = row
        self.column = column
        self.setMinimumSize(240, 130)
        self.state_iconBar = state_iconBar
        self.self_sync = self_sync # for elements like basic_sched or binancesched
        self.config = config

        
        # flag indicates if programm should stop in debugging mode
        self.b_debug = False
        # add function dummy
        self.function = Function(None, self.b_debug, row, column)

        # family tree
        self.parent_element = None

        self.label = QLabel()
        self.label.setObjectName('label')
        self.pixmap = QPixmap(pixmap)
        # set background picture
        self.alterPixmap(pixmap)
        
        # layout containes the iconbar and the element picture
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 30, 0)
        # inner_layout contains the element picture and position text
        self.inner_layout = QVBoxLayout()
        # no effect
        self.inner_layout.setContentsMargins(0, 5, 0, 5)
        #self.inner_layout.setSpacing(0)

        self.inner_layout.addWidget(self.label)

        self.labelTxt = QLabel()
        self.labelTxt.setText('')
        self.labelTxt.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.inner_layout.addWidget(self.labelTxt)

        self.icon_bar = IconBar()
        self.layout.addWidget(self.icon_bar)
        self.icon_bar.del_sig.connect(self.del_element)
        self.icon_bar.edit_sig.connect(self.edit_element)
        self.icon_bar.debug_sig.connect(self.toggle_debug)

        # if not desired hide
        if not self.state_iconBar:
            self.icon_bar.setVisible(False)
        else:
            # else show additional the grid position
            self.updateElementPos()


        self.element_Widget = QWidget()
        self.element_Widget.setLayout(self.inner_layout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.element_Widget)
        self.setLayout(self.layout)

        # when mouse is pressed on the symbol
        self.label.mousePressEvent = self.mousePressEvent
        # when the debug_button is pressed


    def updateElementPos(self):

        logging.debug('ElementMaster::updateElementPos() called row: {}  column: {}'.format(
            self.row, self.column))

        if not self.state_iconBar:
            return

        self.labelTxt.setText('{}|{}    '.format(self.row, alphabet[self.column]))
        self.inner_layout.addWidget(self.labelTxt)

    def updatePosition(self, row, column):

        self.row = row
        self.column = column
        #update the text
        self.updateElementPos()
        # update the function
        func_type  = type(self.function)
        self.addFunction(func_type)

    def addFunction(self, function):
        
        self.function = function(self.config, self.b_debug, self.row, self.column)

    def setChild(self, child):

        if not hasattr(self, 'child_elements'):
            self.child_elements = []

        self.child_elements.append(child)

    def delChild(self, child):
        if child in self.child_elements:
            self.child_elements.remove(child)

    def getChildPos(self):

        if not hasattr(self, 'child_elements'):
            return []
        else:
            return self.child_elements
    
    def getPos(self):

        return (self.row, self.column)

    def listChild(self):
        print('listChild() own type: ', self)
        print('listChild() own position: ', (self.getPos()))
        if self.parent_element:
            print('listChild() parent element: ', (self.parent_element.row,
                self.parent_element.column))
            print('listChild() parent type: ', self.parent_element)
        print('listChild() list logic child elements')
        try:
            for child in self.child_elements:
                print((child.row, child.column))
                print('type: ', child)
        except:
            print('listChild() no childs yet')
        print('func_type  = {}'.format(type(self.function)))

    def del_element(self):
        self.del_sig.emit(self.row, self.column)

    def edit_element(self):
        logging.debug('ElementMaster::edit_element() called MasterItem')
        self.edit_sig.emit()

    def alterPixmap(self, pixmap):

        self.pixmap = pixmap
        self.label.setStyleSheet('#label { background-color: #636363;\
                border: 3px solid #ff5900; border-radius: 20px; }')

        self.label.setPixmap(self.pixmap.scaled(160, 80, Qt.KeepAspectRatio))

    def toggle_debug(self, b_debug):
        logging.debug('toggle_debug() called, b_debug set to {}'.format(b_debug))
        self.b_debug = b_debug
        self.function.b_debug = b_debug

    def highlightStart(self):
        logging.debug('highlightStart() called ElementMaster at {}'.format((self.row, self.column)))
        self.label.setStyleSheet('#label { background-color: #636363;\
                border: 3px solid #fce96f; border-radius: 20px; }')


    def highlightStop(self):
        logging.debug('highlightStop() called ElementMaster at {}'.format((self.row, self.column)))
        self.label.setStyleSheet('#label { background-color: #636363;\
                border: 3px solid #ff5900; border-radius: 20px; }')

    def highlightException(self):
        logging.debug('highlightStop() called ElementMaster at {}'.format((self.row, self.column)))
        self.label.setStyleSheet('#label { background-color: #636363;\
                border: 3px solid #ff0000; border-radius: 20px; }')

    def mousePressEvent(self, event):
            
        logging.debug('ElementMaster::mousePressEvent() called')
        # uncomment this for debugging purpose
        #self.listChild()

        if event.buttons() != Qt.LeftButton:
            return

        icon = QLabel()

        mimeData = QMimeData()
        mime_text = str(self.row) + str(self.column) + str(self.__class__.__name__)
        mimeData.setText(mime_text)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(self.pixmap)
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        if drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction) == Qt.MoveAction:
            icon.close()
        else:
            icon.show()
            icon.setPixmap(self.pixmap)

