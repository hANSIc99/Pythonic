from elementmaster import ElementMaster
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QTextEdit, QWidget,
        QComboBox, QCheckBox, QGridLayout, QSpacerItem, QLineEdit, QPushButton)
from PyQt5.QtCore import QCoreApplication as QC
import logging
from Pythonic.elementeditor import ElementEditor
from Pythonic.record_function import Record, Function


class ExecProcess(ElementMaster):

    pixmap_path = 'images/ExecProcess.png'
    child_pos = (True, True)
    start_branch = pyqtSignal(int, int, name='start_branch')
    
    query_grid = pyqtSignal(name='query_grid')

    def __init__(self, row, column):
        self.row = row
        self.column = column
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, None)
        super().edit_sig.connect(self.edit)
        logging.debug('ExecProcess called at row {}, column {}'.format(row, column))
        self.addFunction(ProcessFunction)


    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecBranch')
        self.row, self.column = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, None)
        super().edit_sig.connect(self.edit)
        self.addFunction(ProcessFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecBranch')
        return (self.row, self.column)


    def edit(self):
        logging.debug('edit() called ExecBranch')
        self.procEditLayout = QVBoxLayout()

        self.procEdit = ElementEditor(self)
        self.procEdit.setWindowTitle(QC.translate('', 'Edit Process Branch'))

        self.help_text = QLabel()
        self.help_text.setText(QC.translate('', 'Multiprocessing: Start a new execution path.')) 

        self.procEditLayout.addWidget(self.help_text)
        self.procEditLayout.addStretch(1)
        self.procEdit.setLayout(self.procEditLayout)

        
        self.procEdit.show()

    def edit_done(self):
        logging.debug('edit_done() called ExecBranch')

    def windowClosed(self, event):
        logging.debug('windowClosed() called ExecBranch')


class ProcessFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):
        #record = 'Hello from ProcessElement {}'.format((self.row, self.column))
        target_0 = (self.row +1, self.column)
        target_1 = (self.row, self.column +1)
        result = Record(self.getPos(), target_0, record, target_1, record)
        return result

