from  masteritem import MasterItem
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox
import logging
from time import sleep


class ExecBranch(MasterItem):

    pixmap_path = 'images/branch.png'

    def __init__(self, row, column):
        self.row = row
        self.column = column
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True)
        super().edit_sig.connect(self.edit)
        logging.debug('ExecBranch called at row {}, column {}'.format(row, column))

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecBranch')
        self.row, self.column = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecBranch')
        return (self.row, self.column)


    def edit(self):
        logging.debug('edit() called ExecBranch')
        self.branchEditLayout = QVBoxLayout()

        self.branchEdit = QWidget(self)
        self.branchEdit.setMinimumSize(500, 400)
        self.branchEdit.setWindowFlags(Qt.Window)
        self.branchEdit.setWindowModality(Qt.WindowModal)
        self.branchEdit.setWindowTitle('Edit Branch')


        self.selectCondition = QComboBox()
        self.selectCondition.addItem('Greater than (>) ...', QVariant('>'))
        self.selectCondition.addItem('Greater or equal than (>=) ...', QVariant('>='))
        self.selectCondition.addItem('Less than (<) ...', QVariant('<'))
        self.selectCondition.addItem('Less or equal than (<=) ...', QVariant('<='))
        self.selectCondition.addItem('equal to (==) ...', QVariant('=='))
        self.selectCondition.addItem('NOT equal to (!=) ...', QVariant('!='))

        self.checkNegate = QCheckBox('Negate query (if NOT ... )')
        self.checkNegate.stateChanged.connect(self.negate_changed)
        self.if_text_1 = QLabel()
        self.if_text_1.setText('if INPUT is ...')

        self.branchEditLayout.addWidget(self.checkNegate)
        self.branchEditLayout.addWidget(self.if_text_1)
        self.branchEditLayout.addWidget(self.selectCondition)
        self.branchEditLayout.addStretch(1)
        self.branchEdit.setLayout(self.branchEditLayout)
        self.branchEdit.show()

    def negate_changed(self, e):
        logging.debug('state changed : {}'.format(e))
        if e == 2:
            self.if_text_1.setText('if NOT INPUT is ...')
        else:
            self.if_text_1.setText('if INPUT is ...')


    def execute(self, data):
        logging.info('execute() called at Item {} {}'.format(self.row, self.column))
        self.highlightStart()
        QCoreApplication.processEvents()
        sleep(1)
        self.highlightStop()
        QCoreApplication.processEvents()

        output = ('output from ExecOp')
        target = (self.row, self.column+1)
        return (target, output)


