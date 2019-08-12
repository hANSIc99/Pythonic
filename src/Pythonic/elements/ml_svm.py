from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, pyqtSlot, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor, QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox, QStackedWidget
from elementeditor import ElementEditor
from PyQt5.QtCore import QCoreApplication as QC
from pythonic_binance.client import Client
import pandas as pd
import os.path, datetime, logging, requests, json
from time import sleep
from Pythonic.record_function import Record, Function
from Pythonic.elementmaster import ElementMaster
from email.message import EmailMessage
from email.contentmanager import raw_data_manager
from sys import getsizeof
#from smtplib import SMTP

class MLSVM(ElementMaster):

    pixmap_path = 'images/MLSVM.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        # pass_input, url, log_state

        pass_input  = False
        url         = None
        log_state   = False

        self.config = pass_input, url, log_state

        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('MLSVM::__init__() called at row {}, column {}'.format(row, column))
        self.addFunction(MLSVMFunction)

    def __setstate__(self, state):
        logging.debug('MLSVM::__setstate__() called')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(MLSVMFunction)

    def __getstate__(self):
        logging.debug('MLSVM::__getstate__() called')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('MLSVM::openEditor() called')

    def edit(self):

        logging.debug('MLSVM::edit()')

        """
        gamma: auto oder float eingabe
        decision function shape: ovr oder ovo

        data split train / eval
        """
        
        self.train_test_label = QLabel()
        self.train_test_label.setText(
                QC.translate('', 'Choose train / evalutaion ratio:'))

        self.train_test_list = QComboBox()
        self.train_test_list.addItem('90/10', QVariant(90))
        self.train_test_list.addItem('80/20', QVariant(80))
        self.train_test_list.addItem('70/30', QVariant(70))
        self.train_test_list.addItem('60/40', QVariant(60))
        self.train_test_list.addItem('50/50', QVariant(50))

        self.decision_function_label = QLabel()
        self.decision_function_label.setText(QC.translate('', 'Choose decision function shape:'))

        self.decision_function_list = QComboBox()
        self.decision_function_list.addItem('ovo', QVariant('ovo'))
        self.decision_function_list.addItem('ovr', QVariant('ovr'))

        self.gamma_label = QLabel()
        self.gamma_label.setText(QC.translate('', 'Gamma:'))

        self.gamma_list = QComboBox()
        self.gamma_list.addItem('Auto', QVariant('auto'))
        self.gamma_list.addItem('Scaled', QVariant('scaled'))
        self.gamma_list.addItem('Manual', QVariant('manual'))
        
        self.conn_rest_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        """
        self.pass_input_line = QWidget()
        self.pass_input_txt = QLabel()
        self.pass_input_txt.setText(QC.translate('','Use input string as URL?'))
        self.pass_input_check = QCheckBox()
        self.pass_input_line_layout = QHBoxLayout(self.pass_input_line)
        self.pass_input_line_layout.addWidget(self.pass_input_txt)
        self.pass_input_line_layout.addWidget(self.pass_input_check)
        self.pass_input_line_layout.addStretch(1)


        self.url_address_txt = QLabel()
        self.url_address_txt.setText(QC.translate('', 'URL:'))
        self.url_address_input = QLineEdit()
        self.url_address_input.setPlaceholderText(
                QC.translate('', 'https://www.bitstamp.net/api/ticker/'))

        """
        self.help_text_1 = QLabel()
        self.help_text_1.setText(QC.translate('', 'GET answer is transformed to Python list object'))

        

        # hier logging option einfügen
        self.log_line = QWidget()
        self.ask_for_logging = QLabel()
        self.ask_for_logging.setText(QC.translate('', 'Log output?'))
        self.log_checkbox = QCheckBox()
        self.log_line_layout = QHBoxLayout(self.log_line)
        self.log_line_layout.addWidget(self.ask_for_logging)
        self.log_line_layout.addWidget(self.log_checkbox)
        self.log_line_layout.addStretch(1)

        
        self.conn_mail_edit = ElementEditor(self)
        self.conn_mail_edit.setWindowTitle(QC.translate('', 'Support Vector Machine'))

        """
        # signals and slots
        self.confirm_button.clicked.connect(self.conn_mail_edit.closeEvent)
        self.conn_mail_edit.window_closed.connect(self.edit_done)
        self.pass_input_check.stateChanged.connect(self.toggle_url_input)

        # load config
        self.loadLastConfig()
        """

        self.conn_rest_layout.addWidget(self.train_test_label)
        self.conn_rest_layout.addWidget(self.train_test_list)
        self.conn_rest_layout.addWidget(self.decision_function_label)
        self.conn_rest_layout.addWidget(self.decision_function_list)
        self.conn_rest_layout.addWidget(self.gamma_label)
        self.conn_rest_layout.addWidget(self.gamma_list)
        self.conn_rest_layout.addWidget(self.help_text_1)
        self.conn_rest_layout.addWidget(self.log_line)
        self.conn_rest_layout.addWidget(self.confirm_button)
        self.conn_mail_edit.setLayout(self.conn_rest_layout)
        self.conn_mail_edit.show()

    def loadLastConfig(self):

        logging.debug('MLSVM::loadLastConfig() called')
        # pass_input, url, log_state
        pass_input, url, log_state = self.config

        self.pass_input_check.setChecked(pass_input)        
        self.log_checkbox.setChecked(log_state)

        if url:
            self.url_address_input.setText(url)

        

    def toggle_url_input(self, event):

        logging.debug('MLSVM::toggle_url_input() called')
        if event == 0:
            self.url_address_input.setDisabled(False)
        else:
            self.url_address_input.setDisabled(True)



    def edit_done(self):

        logging.debug('MLSVM::edit_done() called')

        # pass_input, url, log_state

        pass_input  = self.pass_input_check.isChecked()
        url         = self.url_address_input.text()
        log_state   = self.log_checkbox.isChecked()

        self.config = pass_input, url, log_state
        logging.debug('########CONFIG: {}'.format(self.config))

        self.addFunction(MLSVMFunction)

class MLSVMFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        logging.debug('MLSVMFunction::__init__() called')

    def execute(self, record):

        # pass_input, url, log_state
        pass_input, url, log_state = self.config

        if pass_input:
            recv_string = requests.get(str(record))
        else:
            recv_string = requests.get(url)

        record = json.loads(recv_string.text)


        log_txt = '{REST call succesfull}'
        log_output = '{} bytes received'.format(getsizeof(recv_string.text))

        result = Record(self.getPos(), (self.row +1, self.column), record,
                 log=log_state, log_txt=log_txt, log_output=log_output)

        
        return result
