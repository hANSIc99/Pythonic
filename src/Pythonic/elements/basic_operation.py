from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QWidget,
        QCheckBox, QSpacerItem, QGridLayout, QPushButton, QLineEdit)
from PyQt5.QtCore import QCoreApplication as QC
import logging, os, tempfile, random, subprocess, Pythonic
from Pythonic.elementmaster import ElementMaster, alphabet
from Pythonic.elementeditor import ElementEditor
from Pythonic.record_function import Record, Function

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
        self.cmd_line_txt_2.setText(QC.translate('', 'Use keyword PYFILE to specify the code file.'))
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
            self.code_input.setPlaceholderText(self.placeholder_1 + '\r\n\r\n' +
                                           'print(input)\r\n\r\n' +
                                           self.placeholder_2 +
                                           '\r\n\r\n' + 'output = 5\r\n\r\n' + 
                                           self.placeholder_3 + '\r\n\r\n' +
                                           'log_txt = "debug text"')

        if cmd:
            self.custom_editor_cmd.setText(cmd)
        else:
            self.custom_editor_cmd.setPlaceholderText('tbd')

        if custom_edit_state:
            self.code_input.setEnabled(False)
            self.custom_editor_cmd.setEnabled(True)
            self.openCustomEditor(cmd, code_input)
        else:
            self.code_input.setEnabled(True)
            self.custom_editor_cmd.setEnabled(False)

        
    def openCustomEditor(self, cmd, code_input):
        logging.debug('ExecOp::openCustomEditor() called')
        filename = '{}_{}_{}'.format(self.row, alphabet[self.column], int(random.random() * 1e7))
        filename = os.path.join(tempfile.gettempdir(), filename)
        logging.debug('ExecOp::openCustomEditor() filename: {}'.format(filename))

        try:
            # create new file
            with open(filename, 'w') as f:
                f.write(code_input)
        except Exception as e:
            # not writeable?
            return e
        # subprocess.call('vim', shell=True)
        os.system('vim')

        logging.debug('ExecOp::openCustomEditor() subprocess called')
        #os.remove(filename)

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

class OperationFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):

        log_state, code_input, custom_edit_state, cmd = self.config

        proc_dict = {'record' : record, 'input' : None, 'output' : None, 'log_txt' : None}
                        

        exec_string = 'input = record\r\n'
        exec_string += 'output = record\r\n'

                #logging.warning('Exec-String:\r\n{}'.format(exec_string))
        
        if code_input:
            #logging.warning('Appending user specific code')
            exec_string += code_input


        exec(exec_string, proc_dict)

        output = proc_dict['output']
        log_txt = proc_dict['log_txt']
        if log_txt:
            log_txt = '{{BASIC OPERATION}}        {}'.format(proc_dict['log_txt'])
        else:
            log_txt = '{{BASIC OPERATION}}        {}'.format(proc_dict['output'])

        output = filename
        result = Record(self.getPos(), (self.row+1, self.column), output, log=log_state, log_txt=log_txt)
                
        return result

