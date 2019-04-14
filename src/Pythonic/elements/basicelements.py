from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox
import logging, os.path
from time import sleep
from datetime import datetime
from multiprocessing import Process
from Pythonic.record_function import Record, Function
from Pythonic.dropbox import DropBox
from Pythonic.elements.basic_sched import ExecSched
from Pythonic.elementmaster import ElementMaster

class StartElement(ExecSched):

    pixmap_path = 'images/start.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column
        super().__init__(self.row, self.column)


class ExecRB(ElementMaster):

    pixmap_path = 'images/right_bot.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), False, None)
        logging.debug('ExecRB called at row {}, column {}'.format(row, column))
        self.addFunction(ExecRBFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecRB')
        self.row, self.column = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), False, None)
        self.addFunction(ExecRBFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecRB')
        return (self.row, self.column)

class ExecRBFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):
        result = Record(self.getPos(), (self.row +1, self.column), record)
        return result


class ExecR(ElementMaster):

    pixmap_path = 'images/right.png'
    child_pos = (False, True)

    def __init__(self, row, column):
        self.row = row
        self.column = column
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), False, None)

        logging.debug('ExecR called at row {}, column {}'.format(row, column))
        self.addFunction(ExecRFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecR')
        self.row, self.column = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), False, None)
        self.addFunction(ExecRFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecR')
        return (self.row, self.column)


class ExecRFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):
        result = Record(self.getPos(), (self.row, self.column+1), record)
        return result


class PlaceHolder(ElementMaster):

    # function is connected to add_func() of Workingarea
    func_drop = pyqtSignal(int, int, str, str, name='func_block_drop')
    #query_config = pyqtSignal(int, int, name='query_config')
    pixmap_path = 'images/placeholder.png'
    child_pos = (False, False)

    def __init__(self, row, column):

        self.row = row
        self.column = column
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), False, None)
        #self.setAttribute(Qt.WA_DeleteOnClose)
        logging.debug('PlaceHolder called at row {}, column {}'.format(row, column))
        # everything else
        self.setAcceptDrops(True)
        self.addFunction(PlaceHolderFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called PlaceHolder')
        self.row, self.column = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), False, None)
        self.addFunction(PlaceHolderFunction)
        self.setAcceptDrops(True)

    def __getstate__(self):
        logging.debug('__getstate__() called Placeholder')
        return (self.row, self.column)

    def dropEvent(self, e):

        if e.mimeData().hasText():
            logging.debug('PlaceHolder::dropEvent() mime data: {}'.format(e.mimeData().text()))
            logging.debug('PlaceHolder::dropEvent() event: {}'.format(e.source()))
            self.func_drop.emit(self.row, self.column, e.mimeData().text(), type(e.source()).__name__)
            # DropBox is of type <class 'sip.wrappertype'>
            """
            if (type(e.source()).__name__ == DropBox.__name__):
                logging.debug('PlaceHolder::dropEvent() query config')
                self.query_config.emit(self.row, self.column)
            """

    def dragEnterEvent(self, e):

        logging.debug('PlaceHolder::dragEnterEvent() at pos: {}'.format(e.pos()))
        if e.mimeData().hasText():
            logging.debug('PlaceHolder::dragLeaveEvent() mime data: {}'.format(e.mimeData().text()))
            logging.debug('PlaceHolder::dragEnterEvent() event: {}'.format(e))
            newImg = 'images/' +  e.mimeData().text() + '.png'
            if os.path.isfile(newImg):
                self.alterPixmap(QPixmap(newImg))
                e.accept()

    def dragLeaveEvent(self, e):

        logging.debug('dragLeaveEvent() called')
        self.alterPixmap(QPixmap('images/placeholder.png'))
        e.accept()


class PlaceHolderFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):
        result = Record(self.getPos(), None, record)
        return result


