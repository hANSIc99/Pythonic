from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QWidget,
        QCheckBox, QSpacerItem, QGridLayout, QPushButton, QLineEdit)
from PyQt5.QtCore import QCoreApplication as QC
from PyQt5.QtCore import QProcess
import logging, os, tempfile, random, subprocess, Pythonic, time
from Pythonic.elementmaster import ElementMaster
from Pythonic.elements.basic_operation_func import OperationFunction
from Pythonic.elementeditor import ElementEditor
from Pythonic.record_function import alphabet

class ExecOp(ElementMaster):

    pixmap_path = 'images/ExecOp.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column
        # log_state, code_input, custom_edit_state, cmd
        self.config = (False, None, False, None)
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('ExecOp called at row {}, column {}'.format(row, column))
        self.addFunction(OperationFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecOp')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        self.addFunction(OperationFunction)
        super().edit_sig.connect(self.edit)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecOp')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called ExecOp')

    def edit(self):

        logging.debug('edit() called ExecOp')
        mod_path = os.path.dirname(Pythonic.__file__)

        self.opEditLayout = QVBoxLayout()

        self.op_edit = ElementEditor(self)
        self.op_edit.setWindowTitle(QC.translate('', 'Edit Basic Operation'))

        self.head_info = QLabel()
        self.head_info.setText(QC.translate('', 'Enter your Python 3 code below:'))

        self.help_text = QLabel()
        self.help_text.setText(QC.translate('', 'Process your own Python 3 code.'))

        self.cmd_line_txt_1 = QLabel()
        self.cmd_line_txt_1.setText(QC.translate('', 'Use custom editor?'))
        self.cmd_line_txt_2 = QLabel()
        self.cmd_line_txt_2.setText(QC.translate('', 'Use keyword $FILENAME to specify the code file.'))
        self.cmd_line_txt_3 = QLabel()
        self.cmd_line_txt_3.setText(QC.translate('','Re-open to activate settings.'))

        self.custom_editor_checkbox = QCheckBox()
        self.custom_editor_cmd = QLineEdit()
        self.custom_editor_line = QWidget()
        self.custom_editor_line_layout = QHBoxLayout(self.custom_editor_line)
        self.custom_editor_line_layout.addWidget(self.cmd_line_txt_1)
        self.custom_editor_line_layout.addWidget(self.custom_editor_checkbox)


        self.op_image = QLabel()
        self.op_image.setPixmap(QPixmap(os.path.join(mod_path, self.pixmap_path)))

        self.code_input = QTextEdit()
        self.code_input.setMinimumHeight(250)

        # hier logging option einfügen
        self.log_line = QWidget()
        self.ask_for_logging = QLabel()
        self.ask_for_logging.setText(QC.translate('', 'Log output?'))
        self.log_checkbox = QCheckBox()
        self.log_line_layout = QHBoxLayout(self.log_line)
        self.log_line_layout.addWidget(self.ask_for_logging)
        self.log_line_layout.addWidget(self.log_checkbox)
        self.log_line_layout.addStretch(1)

        self.loadLastConfig()

        
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.spacer = QSpacerItem(0, 30)
        self.picto_spacer = QSpacerItem(0, 40)

        self.picto_widget = QWidget()
        self.pictogram_layout = QGridLayout(self.picto_widget)
        self.pictogram_layout.addWidget(self.op_image, 0, 0)
        self.pictogram_layout.addItem(self.picto_spacer, 0, 1)
        self.pictogram_layout.addWidget(self.help_text, 0, 2)

        self.opEditLayout.addWidget(self.head_info)
        self.opEditLayout.addWidget(self.code_input)
        self.opEditLayout.addWidget(self.custom_editor_line)
        self.opEditLayout.addWidget(self.custom_editor_cmd)
        self.opEditLayout.addWidget(self.cmd_line_txt_2)
        self.opEditLayout.addWidget(self.cmd_line_txt_3)
        self.opEditLayout.addWidget(self.log_line)
        self.opEditLayout.addSpacerItem(self.spacer)
        self.opEditLayout.addWidget(self.picto_widget)
        self.opEditLayout.addWidget(self.confirm_button)
        self.op_edit.setLayout(self.opEditLayout)

        # signals and slots
        self.custom_editor_checkbox.stateChanged.connect(self.toggle_custom_editor)
        self.confirm_button.clicked.connect(self.op_edit.closeEvent)
        self.op_edit.window_closed.connect(self.edit_done)

        self.op_edit.setMinimumHeight(650)
        self.op_edit.show()

    def toggle_custom_editor(self, event):
        logging.debug('ExecOp::toggle_custom_editor() called {}'.format(event))
        if event == 2: #custom editor enabled
            self.code_input.setEnabled(False)
            self.custom_editor_cmd.setEnabled(True)
        else:
            self.code_input.setEnabled(True)
            self.custom_editor_cmd.setEnabled(False)



    def loadLastConfig(self):
        logging.debug('ExecOp::loadLastConfig() called')
        log_state, code_input, custom_edit_state, cmd = self.config

        self.log_checkbox.setChecked(log_state)
        self.custom_editor_checkbox.setChecked(custom_edit_state)

        if code_input:
            self.code_input.setPlainText(code_input)
        else:
            self.placeholder_1 = QC.translate('',
                    '""" use the variable input to access data from previous elements """')
            self.placeholder_2 = QC.translate('',
                    '""" set the output variable to pass data to following elements """')
            self.placeholder_3 = QC.translate('',
                    '""" set the variable log_txt to adjust the logging text """')
            self.placeholder_4 = QC.translate('',
                    '""" use the variable callback to pass data without returning """')
            self.code_input.setPlaceholderText(self.placeholder_1 + '\r\n\r\n' +
                                           'print(input)\r\n\r\n' +
                                           self.placeholder_2 +
                                           '\r\n\r\n' + 'output = 5\r\n\r\n' + 
                                           self.placeholder_3 + '\r\n\r\n' +
                                           self.placeholder_4 + '\r\n\r\n' +
                                           'log_txt = "debug text"')

        if cmd:
            self.custom_editor_cmd.setText(cmd)
        else:
            if os.name == 'nt':
                self.custom_editor_cmd.setPlaceholderText(r'C:\"Program Files (x86)"\Notepad++\notepad++.exe $FILENAME')
            else:
                self.custom_editor_cmd.setPlaceholderText('gnome-terminal --wait -e "vim $FILENAME"')
            
        if custom_edit_state:
            self.code_input.setEnabled(False)
            self.custom_editor_cmd.setEnabled(True)
            self.openCustomEditor(cmd, code_input)
        else:
            self.code_input.setEnabled(True)
            self.custom_editor_cmd.setEnabled(False)

        
    def openCustomEditor(self, cmd, code_input):
        logging.debug('ExecOp::openCustomEditor() called')
        filename = '{}_{}_{}.py'.format(self.row, alphabet[self.column], int(random.random() * 1e7))
        filename = os.path.join(tempfile.gettempdir(), filename)
        logging.debug('ExecOp::openCustomEditor() filename: {}'.format(filename))


        
        if cmd:
            try:
                # create new file
                with open(filename, 'w') as f:
                    if code_input:
                        f.write(code_input)
            except Exception as e:
                # not writeable?
                return e

            cmd = cmd.replace('$FILENAME', filename)
        else:
            logging.debug('ExecOp::openCustomEditor() no command specified - returning')
            return

        logging.debug('ExecOp::openCustomEditor() cmd: {}'.format(cmd))
        logging.debug('ExecOp::openCustomEditor() subprocess called')
        edit_proc = QProcess()
        edit_proc.start(cmd)
        edit_proc.waitForFinished(-1)

        logging.debug('ExecOp::openCustomEditor() subprocess ended')

        try:
            # create new file
            with open(filename, 'r') as f:
                code_input = f.read()
        except Exception as e:
            # not writeable?
            return e

        self.code_input.setPlainText(code_input)
        logging.debug('ExecOp::openCustomEditor() removing temporary file')
        os.remove(filename)

    def edit_done(self):
        logging.debug('edit_done() called ExecOp' )

        if self.code_input.toPlainText() == '':
            code_input = None
        else:
            code_input = self.code_input.toPlainText()

        if self.custom_editor_cmd.text() == '':
            cmd = None
        else:
            cmd = self.custom_editor_cmd.text()

        custom_edit_state = self.custom_editor_checkbox.isChecked()

        self.config = (self.log_checkbox.isChecked(), code_input, custom_edit_state, cmd)
        self.addFunction(OperationFunction)
        logging.debug('edit_done() 2 called ExecOp' )
