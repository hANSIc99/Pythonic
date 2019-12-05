from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import  QPixmap
import logging, os, Pythonic
from Pythonic.dropbox import DropBox
from Pythonic.elements.basic_sched import ExecSched
from Pythonic.elementmaster import ElementMaster
from Pythonic.elements.basicelements_func import ExecRFunction, ExecRBFunction, PlaceHolderFunction

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
        super().__init__(self.row, self.column, self.pixmap_path, False, None)
        logging.debug('ExecRB called at row {}, column {}'.format(row, column))
        self.addFunction(ExecRBFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecRB')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, False, None)
        self.addFunction(ExecRBFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecRB')
        return (self.row, self.column, self.config)

class ExecR(ElementMaster):

    pixmap_path = 'images/right.png'
    child_pos = (False, True)

    def __init__(self, row, column):
        self.row = row
        self.column = column
        super().__init__(self.row, self.column, self.pixmap_path, False, None)

        logging.debug('ExecR called at row {}, column {}'.format(row, column))
        self.addFunction(ExecRFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecR')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, False, None)
        self.addFunction(ExecRFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecR')
        return (self.row, self.column, self.config)

class PlaceHolder(ElementMaster):

    # function is connected to add_func() of Workingarea
    func_drop = pyqtSignal(int, int, str, str, name='func_block_drop')
    #query_config = pyqtSignal(int, int, name='query_config')
    pixmap_path = 'images/placeholder.png'
    child_pos = (False, False)

    def __init__(self, row, column):

        self.row = row
        self.column = column
        self.mod_path = os.path.dirname(Pythonic.__file__)
        super().__init__(self.row, self.column, self.pixmap_path, False, None)
        logging.debug('PlaceHolder called at row {}, column {}'.format(row, column))
        # everything else
        self.setAcceptDrops(True)
        self.addFunction(PlaceHolderFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called PlaceHolder')
        self.mod_path = os.path.dirname(Pythonic.__file__)
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, False, None)
        self.addFunction(PlaceHolderFunction)
        self.setAcceptDrops(True)

    def __getstate__(self):
        logging.debug('__getstate__() called Placeholder')
        return (self.row, self.column, self.config)

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
            newImg = self.mod_path + '/images/' +  e.mimeData().text() + '.png'
            if os.path.isfile(newImg):
                self.alterPixmap(QPixmap(newImg))
                e.accept()

    def dragLeaveEvent(self, e):

        logging.debug('dragLeaveEvent() called')
        self.alterPixmap(QPixmap(os.path.join(self.mod_path, 'images/placeholder.png')))
        e.accept()
