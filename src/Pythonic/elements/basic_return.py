from elementmaster import ElementMaster, alphabet
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox,
                                QPushButton)
from PyQt5.QtCore import QCoreApplication as QC
import logging
import os.path
from time import sleep
from datetime import datetime
from Pythonic.elementmaster import alphabet
from Pythonic.elementeditor import ElementEditor
from Pythonic.record_function import Record, Function

class ExecReturn(ElementMaster):

    pixmap_path = 'images/ExecReturn.png'
    child_pos = (False, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        # currentdata, currentindex, ischecked
        self.config = (None, None, False)
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('ExecReturn called at row {}, column {}'.format(row, column))

        self.addFunction(ReturnFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecReturn')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(ReturnFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecReturn')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called ExecReturn')

    def edit(self):
        logging.debug('edit() called ExecReturn')
        self.returnEditLayout = QVBoxLayout()

        self.returnEdit = ElementEditor(self)
        self.returnEdit.setWindowTitle(QC.translate('', 'Edit Return'))

        self.top_text = QLabel()
        self.top_text.setText(QC.translate('', 'Go to element:'))

        self.help_text = QWidget()
        self.help_text_layout = QVBoxLayout(self.help_text)

        self.help_text_1 = QLabel()
        self.help_text_1.setText(QC.translate('', 'Choose an element from the list')) 

        self.help_text_2 = QLabel()
        self.help_text_2.setText(QC.translate('', 'to which you want to return with the'))

        self.help_text_3 = QLabel()
        self.help_text_3.setText(QC.translate('', 'current input'))

        self.help_text_layout.addWidget(self.help_text_1)
        self.help_text_layout.addWidget(self.help_text_2)
        self.help_text_layout.addWidget(self.help_text_3)


        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        # hier logging option einfügen
        self.log_line = QWidget()
        self.ask_for_logging = QLabel()
        self.ask_for_logging.setText(QC.translate('', 'Log output?'))
        self.log_checkbox = QCheckBox()
        self.log_line_layout = QHBoxLayout(self.log_line)
        self.log_line_layout.addWidget(self.ask_for_logging)
        self.log_line_layout.addWidget(self.log_checkbox)
        self.log_line_layout.addStretch(1)


        self.element_selector = QComboBox()
        self.populateSelector()

        if self.config[1]:
            self.element_selector.setCurrentIndex(self.config[1])
        if self.config[2]:
            self.log_checkbox.setChecked(True)

        self.confirm_button.clicked.connect(self.returnEdit.closeEvent)
        self.returnEdit.window_closed.connect(self.edit_done)
        self.returnEditLayout.addWidget(self.top_text)
        self.returnEditLayout.addWidget(self.element_selector)
        self.returnEditLayout.addWidget(self.log_line)
        self.returnEditLayout.addWidget(self.help_text)
        self.returnEditLayout.addStretch(1)
        self.returnEditLayout.addWidget(self.confirm_button)
        self.returnEdit.setLayout(self.returnEditLayout)
        self.returnEdit.show()

    def populateSelector(self):

        index = self.parent().returnCurrentElements()

        for pos in index:
            if self.getPos() != pos:
                self.element_selector.addItem('{} {}'.format(pos[0], alphabet[pos[1]]), QVariant(pos))

    def edit_done(self):
        logging.debug('edit_done() called ExecReturn' )
        self.config = (self.element_selector.currentData(), self.element_selector.currentIndex(), self.log_checkbox.isChecked())
        self.addFunction(ReturnFunction)

class ReturnFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):

        log_txt = '{{BASIC RETURN}}           Return to {}|{}'.format(self.config[0][0], alphabet[self.config[0][1]])
        result = Record(self.getPos(), self.config[0], record, log=self.config[2], log_txt=log_txt)
        return result

