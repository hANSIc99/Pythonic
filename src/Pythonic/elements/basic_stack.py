from elementmaster import ElementMaster, alphabet
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox, QFileDialog, QPushButton, QStackedWidget)
from record_function import Record, Function
from elementeditor import ElementEditor
from PyQt5.QtCore import QCoreApplication as QC
import logging
from time import sleep
from datetime import datetime
from elementmaster import alphabet
import os.path

class ExecStack(ElementMaster):

    pixmap_path = 'images/ExecStack.png'
    child_pos = (False, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        # filename, log_state 
        self.config = (None, False)
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('ExecStack called at row {}, column {}'.format(row, column))

        self.addFunction(StackFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecStack')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(StackFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecStack')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called ExecStack')

    def edit(self):
        logging.debug('edit() called ExecStack')

        self.filename, log_state = self.config

        self.returnEditLayout = QVBoxLayout()

        self.returnEdit = ElementEditor(self)
        self.returnEdit.setWindowTitle(QC.translate('', 'Stack'))

        self.top_text = QLabel()
        self.top_text.setText(QC.translate('', 'Stack ...'))

        self.filename_text = QLabel()
        if self.filename:
            self.filename_text.setText(self.filename)
        else:
            self.filename_text.setText(QC.translate('', 'Filename'))

        self.file_button = QPushButton(QC.translate('', 'Choose file'))
        self.file_button.clicked.connect(self.ChooseFileDialog)

        self.variable_box = QStackedWidget()
        self.writeInput()
        self.readInput()

        self.mode_text = QLabel()
        self.mode_text.setText(QC.translate('', 'Select mode:'))

        self.select_mode = QComboBox()
        self.select_mode.addItem(QC.translate('', 'Write'), QVariant('w'))
        self.select_mode.addItem(QC.translate('', 'Read'), QVariant('r'))

        self.help_text = QWidget()
        self.help_text_layout = QVBoxLayout(self.help_text)

        # Option: Fixed size
        self.help_text_1 = QLabel()
        # Liste
        self.help_text_1.setText(QC.translate('', 'On input: Write / Read')) 


        # Input: Liste
        self.help_text_2 = QLabel()
        self.help_text_2.setText(QC.translate('', 'Insert /Append'))

        # Option: Remove output
        # Output: Liste: First Out /  Last Out / all Out 
        self.help_text_3 = QLabel()
        self.help_text_3.setText(QC.translate('', 'Help Text 3'))

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

        if log_state:
            self.log_checkbox.setChecked(True)

        self.confirm_button.clicked.connect(self.returnEdit.closeEvent)
        self.select_mode.currentIndexChanged.connect(self.indexChanged)
        self.returnEdit.window_closed.connect(self.edit_done)
        self.returnEditLayout.addWidget(self.top_text)
        self.returnEditLayout.addWidget(self.filename_text)
        self.returnEditLayout.addWidget(self.file_button)
        self.returnEditLayout.addWidget(self.mode_text)
        self.returnEditLayout.addWidget(self.select_mode)
        self.returnEditLayout.addWidget(self.variable_box)
        self.returnEditLayout.addWidget(self.help_text)
        self.returnEditLayout.addStretch(1)
        self.returnEditLayout.addWidget(self.log_line)
        self.returnEditLayout.addWidget(self.confirm_button)
        self.returnEdit.setLayout(self.returnEditLayout)
        self.returnEdit.show()

    def ChooseFileDialog(self, event):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, QC.translate('', 'Choose file'),"","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            logging.debug('ChooseFileDialog() called with filename: {}'.format(fileName))
            self.filename = fileName
            self.filename_text.setText(self.filename)

    def writeInput(self):

        self.write_input = QWidget()
        self.write_layout = QHBoxLayout(self.write_input)

        self.write_txt = QLabel()
        self.write_txt.setText(QC.translate('', 'Do this with input:'))

        self.select_write_mode = QComboBox()
        self.select_write_mode.addItem(QC.translate('', 'Insert'), QVariant('i'))
        self.select_write_mode.addItem(QC.translate('', 'Append'), QVariant('a'))


        self.write_layout.addWidget(self.write_txt)
        self.write_layout.addWidget(self.select_write_mode)


        self.variable_box.addWidget(self.write_input)

    def readInput(self):

        self.read_input = QWidget()
        self.read_layout = QHBoxLayout(self.read_input)

        self.read_txt = QLabel()
        self.read_txt.setText(QC.translate('', 'Do this when triggered:'))

        self.select_read_mode = QComboBox()
        self.select_read_mode.addItem(QC.translate('', 'First out'), QVariant('f'))
        self.select_read_mode.addItem(QC.translate('', 'Last out'), QVariant('l'))
        self.select_read_mode.addItem(QC.translate('', 'All out'), QVariant('a'))


        self.read_layout.addWidget(self.read_txt)
        self.read_layout.addWidget(self.select_read_mode)


        self.variable_box.addWidget(self.read_input)

    def indexChanged(self, event):

        current_index = event
        logging.debug('indexChanged() called {}'.format(current_index))
        self.variable_box.setCurrentIndex(current_index)


    def populateSelector(self):

        index = self.parent().returnCurrentElements()

        for pos in index:
            if self.getPos() != pos:
                self.element_selector.addItem(
                        '{} {}'.format(pos[0], alphabet[pos[1]]), QVariant(pos))

    def edit_done(self):
        logging.debug('edit_done() called ExecStack' )
        log_state = self.log_checkbox.isChecked()
        filename = self.filename
        self.config = (filename, log_state)
        self.addFunction(StackFunction)

class StackFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):

        log_txt = '{{BASIC STACK}}           Return to {}|{}'.format(self.config[0][0], alphabet[self.config[0][1]])
        result = Record(self.getPos(), self.config[0], record, log=self.config[2], log_txt=log_txt)
        return result

