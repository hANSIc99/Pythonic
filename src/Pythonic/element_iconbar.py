from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QSizePolicy, QStyleOption, QStyle
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, pyqtSignal
import logging

class EditButton(QLabel):

    edit_pressed = pyqtSignal(name='edit_pressed')

    def __init__(self):
        super().__init__()
        logging.debug('__init__() called EditButton')
        self.setPixmap(QPixmap('images/edit.png').scaled(20, 20))
        self.setStyleSheet('background-color: lightblue; \
                border-style: solid; border-color: lightblue; border-width: 1px')
        self.setMargin(5)


    def enterEvent(self, event):
        self.setStyleSheet('background-color: lightblue; \
                border-style: solid; border-color: white; border-width: 1px')

    def leaveEvent(self, event):
        self.setStyleSheet('background-color: lightblue; \
                border-style: solid; border-color: lightblue; border-width: 1px')

    def mousePressEvent(self, event):
       self.edit_pressed.emit() 

class DebugButton(QLabel):

    debug_pressed = pyqtSignal(bool, name='debug_pressed') 

    def __init__(self):
        super().__init__()
        logging.debug('__init__() called DebugButton')
        self.setPixmap(QPixmap('images/debug.png').scaled(20, 20))
        self.setStyleSheet('background-color: goldenrod; \
                border-style: solid; border-color: goldenrod; border-width: 1px')
        self.setMargin(5)
        self.b_debug = False


    def enterEvent(self, event):
        if self.b_debug:
            self.setStyleSheet('background-color: olivedrab; \
                    border-style: solid; border-color: white; border-width: 1px')
        else:
            self.setStyleSheet('background-color: goldenrod; \
                    border-style: solid; border-color: white; border-width: 1px')

    def leaveEvent(self, event):
        if self.b_debug:
            self.setStyleSheet('background-color: olivedrab; \
                    border-style: solid; border-color: olivedrab; border-width: 1px')
        else:
            self.setStyleSheet('background-color: goldenrod; \
                    border-style: solid; border-color: goldenrod; border-width: 1px')

    def mousePressEvent(self, event):

        if self.b_debug:
            self.b_debug = False
            self.disableStyleClicked()
                
        else:
            self.b_debug = True
            self.enableStyleClicked()
            
        self.debug_pressed.emit(self.b_debug)

    def enableStyleClicked(self):

        self.setStyleSheet('background-color: olivedrab; \
                    border-style: solid; border-color: olivedrab; border-width: 1px')

        

    def disableStyleClicked(self):

        self.setStyleSheet('background-color: goldenrod; \
                    border-style: solid; border-color: goldenrod; border-width: 1px')


    def disableMouseEvent(self): # only called by basic StackWindow
        
        self.b_debug = True
        self.enableStyleClicked()

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def enableMouseEvent(self): # only called by basic StackWindow

        self.b_debug = False
        self.disableStyleClicked()

        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)

class DelButton(QLabel):

    delete_pressed = pyqtSignal(name='delete_pressed')

    def __init__(self):
        super().__init__()
        logging.debug('__init__() called DelButton')
        self.setPixmap(QPixmap('images/del.png').scaled(20, 20))
        self.setStyleSheet('background-color: darkred; \
                border-style: solid; border-color: darkred; border-width: 1px')
        self.setMargin(5)


    def enterEvent(self, event):
        self.setStyleSheet('background-color: darkred; \
                border-style: solid; border-color: white; border-width: 1px')

    def leaveEvent(self, event):
        self.setStyleSheet('background-color: darkred; \
                border-style: solid; border-color: darkred; border-width: 1px')

    def mousePressEvent(self, event):
        self.delete_pressed.emit()

class IconBar(QWidget):

    del_sig = pyqtSignal(name='delete_element')
    edit_sig = pyqtSignal(name='edit_element')
    debug_sig = pyqtSignal(bool, name='edit_element')

    def __init__(self):

        super().__init__()
        logging.debug('__init__() called IconBar')


        #self.setAutoFillBackground(True)
        #self.setGeometry(0, 0, 20, 100)

        self.iconBox = QVBoxLayout()
        self.edit_button = EditButton()
        #self.debug_button = QLabel()
        self.debug_button = DebugButton()
        self.del_button = DelButton()

        policy = QSizePolicy()
        policy.setRetainSizeWhenHidden(True)

        self.setSizePolicy(policy)

        self.iconBox.addWidget(self.edit_button)
        self.iconBox.addWidget(self.debug_button)
        self.iconBox.addWidget(self.del_button)
        
        self.setLayout(self.iconBox)

        self.setObjectName('IconBar')
        self.setStyleSheet('#IconBar { background-color: #636363; border: 3px solid #ff5900; border-radius: 15px; }')


        #self.del_button.mousePressEvent = self.click_del_element
        #self.edit_button.mousePressEvent = self.click_edit_element
        #self.debug_button.mousePressEvent = self.click_debug_element
        self.del_button.delete_pressed.connect(self.click_del_element)
        self.edit_button.edit_pressed.connect(self.click_edit_element)
        self.debug_button.debug_pressed.connect(self.click_debug_element)


    def paintEvent(self, event):
        
        style_opt = QStyleOption()
        style_opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, style_opt, painter, self)

    def click_del_element(self):
        self.del_sig.emit()

    def click_edit_element(self):
        self.edit_sig.emit()

    def click_debug_element(self, b_debug):
        self.debug_sig.emit(b_debug)
         
