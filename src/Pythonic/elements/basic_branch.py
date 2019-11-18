from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QWidget,
        QComboBox, QCheckBox, QGridLayout, QSpacerItem, QLineEdit, QPushButton)
from PyQt5.QtCore import QCoreApplication as QC
import logging, os, Pythonic
from Pythonic.elementeditor import ElementEditor
from Pythonic.record_function import Record, Function, alphabet
from Pythonic.elementmaster import ElementMaster


class ExecBranch(ElementMaster):

    pixmap_path = 'images/ExecBranch.png'
    child_pos = (True, True)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        compare_with = None
        negate = False
        operation = '>'
        log_state = False
        op_index = 0
        # compare_with,  operation, op_index, negate, log_state
        self.config = (compare_with, operation, op_index, negate, log_state)

        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        self.initUI()
        logging.debug('ExecBranch called at row {}, column {}'.format(row, column))

        
    def initUI(self):

        self.selectCondition = QComboBox()
        self.selectCondition.addItem(QC.translate('', 'Greater than (>) ...'), QVariant('>'))
        self.selectCondition.addItem(QC.translate('', 'Greater or equal than (>=) ...'), QVariant('>='))
        self.selectCondition.addItem(QC.translate('', 'Less than (<) ...'), QVariant('<'))
        self.selectCondition.addItem(QC.translate('', 'Less or equal than (<=) ...'), QVariant('<='))
        self.selectCondition.addItem(QC.translate('', 'Equal to (==) ...'), QVariant('=='))
        self.selectCondition.addItem(QC.translate('', 'NOT equal to (!=) ...'), QVariant('!='))
        self.selectCondition.setCurrentIndex(0)

        #self.addFunction(BranchFunction)

    def __setstate__(self, state):
        # BAUSTELLE
        logging.debug('__setstate__() called ExecBranch')
        self.row, self.column, self.config  = state
        self.initUI()
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(BranchFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecBranch')
        return (self.row, self.column, self.config)


    def edit(self):

        logging.debug('edit() called ExecBranch')
        mod_path = os.path.dirname(Pythonic.__file__)

        self.branchEditLayout = QVBoxLayout()

        self.branchEdit = ElementEditor(self)
        self.branchEdit.setWindowTitle(QC.translate('', 'Edit Branch'))

        self.branch_image = QLabel()
        self.branch_image.setPixmap(QPixmap(os.path.join(mod_path, self.pixmap_path)))

        self.branch_yes = QLabel()
        self.branch_yes.setText(QC.translate('', 'Yes'))
        self.branch_yes.setAlignment(Qt.AlignCenter)

        self.branch_no = QLabel()
        self.branch_no.setText(QC.translate('', 'No'))

        self.help_text = QWidget()
        self.help_text_layout = QVBoxLayout(self.help_text)

        self.help_text_1 = QLabel()
        self.help_text_1.setText(QC.translate('', 'Leads the execution path')) 

        self.help_text_2 = QLabel()
        self.help_text_2.setText(QC.translate('', 'according to the defined condition.'))

        self.help_text_3 = QLabel()
        self.help_text_3.setText(QC.translate('', 'Put strings in quotation marks:'))

        self.help_text_4 = QLabel()
        self.help_text_4.setText(QC.translate('', 'e.g. "state_x"'))

        self.help_text_layout.addWidget(self.help_text_1)
        self.help_text_layout.addWidget(self.help_text_2)
        self.help_text_layout.addWidget(self.help_text_3)
        self.help_text_layout.addWidget(self.help_text_4)

        self.spacer = QSpacerItem(0, 30)
        self.picto_spacer = QSpacerItem(40, 0)

        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.picto_widget = QWidget()
        self.pictogram_layout = QGridLayout(self.picto_widget)
        self.pictogram_layout.addWidget(self.branch_image, 0, 0)
        self.pictogram_layout.addWidget(self.branch_yes, 1, 0)
        self.pictogram_layout.addWidget(self.branch_no, 0, 1)
        self.pictogram_layout.addItem(self.picto_spacer, 0, 2)
        self.pictogram_layout.addWidget(self.help_text, 0, 3)
        self.pictogram_layout.setColumnStretch(4, 1)

        
        self.checkNegate = QCheckBox(QC.translate('', 'Negate query (if NOT ... )'))
        # try to load status
        try:
            compare_with, operation, op_index, negate, log_state = self.config
        except TypeError as e:
            pass

        self.selectCondition.setCurrentIndex(op_index)

        if negate:
            self.checkNegate.setChecked(True)

        self.if_text_1 = QLabel()
        self.if_text_1.setText(QC.translate('', 'if INPUT is ...'))

        self.user_input = QLineEdit()
        if compare_with:
            self.user_input.setText(compare_with)

        # hier logging option einfügen
        self.log_line = QWidget()
        self.ask_for_logging = QLabel()
        self.ask_for_logging.setText(QC.translate('', 'Log output?'))
        self.log_checkbox = QCheckBox()
        self.log_line_layout = QHBoxLayout(self.log_line)
        self.log_line_layout.addWidget(self.ask_for_logging)
        self.log_line_layout.addWidget(self.log_checkbox)
        self.log_line_layout.addStretch(1)

        if log_state:
            self.log_checkbox.setChecked(True)

        self.branchEditLayout.addWidget(self.checkNegate)
        self.branchEditLayout.addWidget(self.if_text_1)
        self.branchEditLayout.addWidget(self.selectCondition)
        self.branchEditLayout.addWidget(self.user_input)
        self.branchEditLayout.addWidget(self.log_line)
        self.branchEditLayout.addSpacerItem(self.spacer)
        self.branchEditLayout.addWidget(self.picto_widget)
        self.branchEditLayout.addStretch(1)
        self.branchEditLayout.addWidget(self.confirm_button)
        self.branchEdit.setLayout(self.branchEditLayout)

        # signals and slots
        self.confirm_button.clicked.connect(self.branchEdit.closeEvent)
        self.branchEdit.window_closed.connect(self.edit_done)
        
        self.branchEdit.show()

    def edit_done(self):
        logging.debug('edit_done() called ExecBranch')
        text_input = self.user_input.text()

        if text_input == '':
            compare_with = None
        else:
            compare_with = self.user_input.text()


        operation   = self.selectCondition.currentData()
        op_index    = self.selectCondition.currentIndex()
        negate      = self.checkNegate.isChecked()       
        log_state   = self.log_checkbox.isChecked()

        # compare_with,  operation, op_index, negate, log_state
        self.config = (compare_with, operation, op_index, negate, log_state)

        self.addFunction(BranchFunction)

    def windowClosed(self, event):
        logging.debug('windowClosed() called ExecBranch')

class BranchFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):

        if self.config:
            compare_with, operation, op_index, negate, log_state = self.config
        else:
            result = Record(self.getPos(), None, record)
            return result


        exec_scope = {}
        exec_string = 'result = True if '

        if negate:
            exec_string += 'not '

        if isinstance(record, str):
            exec_string += '"{}" {} {} '.format(record, operation, compare_with)
        else:
            exec_string += '{} {} {} '.format(record, operation, compare_with)

        exec_string += 'else False'

        exec(exec_string, exec_scope)

        logging.info('exec_string: {}'.format(exec_string))
        
        if exec_scope['result']:
            target = (self.row + 1, self.column)
            log_txt = '{{BASIC BRANCH}}           >>TRUE<< go to {}|{}'.format(self.row + 1, alphabet[self.column])
        else:
            target = (self.row, self.column + 1)
            log_txt = '{{BASIC BRANCH}}           <<FALSE>> go to {}|{}'.format(self.row, alphabet[self.column + 1])


        result = Record(self.getPos(), target, record, log=log_state, log_txt=log_txt)
        return result

