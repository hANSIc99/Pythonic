from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, pyqtSlot, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor, QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox, QStackedWidget
from elementeditor import ElementEditor
from PyQt5.QtCore import QCoreApplication as QC
from pythonic_binance.client import Client
import pandas as pd
import os.path, datetime, logging
from time import sleep
from Pythonic.record_function import Record, Function
from Pythonic.elementmaster import ElementMaster

from smtplib import SMTP

class ConnMail(ElementMaster):

    pixmap_path = 'images/ConnMail.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        recipient       = None
        sender          = None
        credentials     = None
        server_url      = None
        server_port     = '465'
        input_opt_index = 0
        input_opt_data  = None
        pass_input      = False
        message_state   = False
        log_state       = False

        # recipient, sender, credentials, server_url, server_port,
        # input_opt_index, input_opt_data, pass_input, message_state, log_state
        self.config = (recipient, sender, credentials, server_url, server_port,
                input_opt_index, input_opt_data, pass_input, message_state, log_state)

        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('BinanceOrder called at row {}, column {}'.format(row, column))
        self.addFunction(ConnMailFunction)

    def __setstate__(self, state):
        logging.debug('ConnMail::__setstate__() called')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(ConnMailFunction)

    def __getstate__(self):
        logging.debug('ConnMail__getstate__() called')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('ConnMail::openEditor() called')

    def edit(self):

        logging.debug('ConnMail::edit()')
        # recipient, sender, credentials, server_url, server_port,
        # input_opt_index, input_opt_data, pass_input, message_state, log_state


        pub_key, prv_key, side_index, side_txt, symbol_txt, quantity, \
                order_index, order_string, order_config, log_state = self.config

        self.conn_mail_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.recipient_address_txt = QLabel()
        self.recipient_address_txt.setText(QC.translate('', 'Recipient address:'))
        self.recipient_address_input = QLineEdit()
        self.recipient_address_input.setPlaceholderText(
                QC.translate('', 'Separate addresses with spaces'))

        self.sender_address_txt = QLabel()
        self.sender_address_txt.setText(QC.translate('', 'Enter sender address:'))
        self.sender_address_input = QLineEdit()
        self.sender_address_input.setPlaceholderText(QC.translate('', 'user@example.com'))

        self.credentials_txt = QLabel()
        self.credentials_txt.setText(QC.translate('', 'Enter credentials:'))
        self.credentials_input = QLineEdit()
        self.credentials_input.setEchoMode(QLineEdit.Password)

        self.subject_txt = QLabel()
        self.subject_txt.setText(QC.translate('', 'Enter subject:'))
        self.subject_input = QLineEdit()

        self.server_txt = QLabel()
        self.server_txt.setText(QC.translate('', 'Enter server URL and port number:'))

        self.server_input_line = QWidget()
        self.server_input_line_layout = QHBoxLayout(self.server_input_line)
        self.server_url_input = QLineEdit()
        self.server_url_input.setPlaceholderText(QC.translate('', 'e.g. smtp.gmail.com'))
        self.server_port_input = QLineEdit()
        self.server_port_input.setMaximumWidth(50)
        self.server_port_input.setValidator(QIntValidator(0, 9999))
        self.server_port_input.setText('465')
        self.server_input_line_layout.addWidget(self.server_url_input)
        self.server_input_line_layout.addWidget(self.server_port_input)


        self.message_box_line = QWidget()
        self.message_box_txt = QLabel()
        self.message_box_txt.setText(QC.translate('', 'Activate user defined message txt?'))
        self.message_box_checkbox = QCheckBox()
        self.message_box_line_layout = QHBoxLayout(self.message_box_line)
        self.message_box_line_layout.addWidget(self.message_box_txt)
        self.message_box_line_layout.addWidget(self.message_box_checkbox)
        self.message_box_line_layout = QHBoxLayout(self.message_box_line)

        self.message_txt_input = QTextEdit()


        self.input_option_line = QWidget()
        self.input_option_txt = QLabel()
        self.input_option_txt.setText(QC.translate('', 'Use input as: '))
        self.input_options = QComboBox()
        self.input_options.addItem(QC.translate('', 'None'))
        self.input_options.addItem(QC.translate('', 'Message txt'))
        self.input_options.addItem(QC.translate('', 'Attachement'))
        self.input_option_line_layout = QHBoxLayout(self.input_option_line)
        self.input_option_line_layout.addWidget(self.input_option_txt)
        self.input_option_line_layout.addWidget(self.input_options)


        self.pass_input_line = QWidget()
        self.pass_input_txt = QLabel()
        self.pass_input_txt.setText(QC.translate('','Pass input forward?'))
        self.pass_input_check = QCheckBox()
        self.pass_input_line_layout = QHBoxLayout(self.pass_input_line)
        self.pass_input_line_layout.addWidget(self.pass_input_txt)
        self.pass_input_line_layout.addWidget(self.pass_input_check)

        self.help_txt = QLabel()
        self.help_txt.setText(QC.translate('', 'Only encrypted connections are allowed'))

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


        self.conn_mail_edit = ElementEditor(self)
        self.conn_mail_edit.setWindowTitle(QC.translate('', 'Place a Order'))
        #self.conn_mail_edit.setMinimumSize(240, 330)

        # signals and slots
        self.confirm_button.clicked.connect(self.conn_mail_edit.closeEvent)
        self.conn_mail_edit.window_closed.connect(self.edit_done)
        self.message_box_checkbox.stateChanged.connect(self.toggle_message_box)

        # load existing config
        

        self.conn_mail_layout.addWidget(self.recipient_address_txt)
        self.conn_mail_layout.addWidget(self.recipient_address_input)
        self.conn_mail_layout.addWidget(self.sender_address_txt)
        self.conn_mail_layout.addWidget(self.sender_address_input)
        self.conn_mail_layout.addWidget(self.credentials_txt)
        self.conn_mail_layout.addWidget(self.credentials_input)
        self.conn_mail_layout.addWidget(self.server_txt)
        self.conn_mail_layout.addWidget(self.server_input_line)
        self.conn_mail_layout.addWidget(self.message_box_line)
        self.conn_mail_layout.addWidget(self.message_txt_input)
        self.conn_mail_layout.addWidget(self.input_option_line)
        self.conn_mail_layout.addWidget(self.pass_input_line)

        self.conn_mail_layout.addWidget(self.help_txt)
        self.conn_mail_layout.addWidget(self.log_line)
        self.conn_mail_layout.addWidget(self.confirm_button)
        self.conn_mail_edit.setLayout(self.conn_mail_layout)
        self.conn_mail_edit.show()
        

    def toggle_message_box(self, event):

        logging.error('State changed {}'.format(event))
        if event == 0:
            self.message_txt_input.setDisabled(True)
        else:
            self.message_txt_input.setDisabled(False)


    def loadLastConfig(self):

        # recipient, sender, credentials, server_url, server_port,
        # input_opt_index, input_opt_data, pass_input, message_state, log_state

        recipient, sender, credentials, server_url, server_port, \
                input_opt_index, input_opt_data, pass_input, message_state, \
                log_state = self.config



    def edit_done(self):

        logging.debug('ConnMail::edit_done() called')

        recipient       = self.recipient_address_input.text()
        sender          = self.sender_address_input.text()
        credentials     = self.credentials_input.text() 
        server_url      = self.server_url_input.text()
        server_port     = self.server_port_input.text()
        input_opt_index = self.input_options.currentIndex()
        input_opt_data  = self.input_options.currentData()

        pass_input      = self.pass_input_check.isChecked()
        message_state   = self.message_box_checkbox.isChecked()   
        log_state       = self.log_checkbox.isChecked()

        if self.message_txt_input.toPlainText() == '':
            message_txt = None
        else:
            message_txt = self.message_txt.toPlainText()
        # recipient, sender, credentials, server_url, server_port,
        # input_opt_index, input_opt_data, pass_input, message_state, log_state
        self.config = (recipient, sender, credentials, server_url, server_port,
                input_opt_index, input_opt_data, pass_input, message_state, log_state)

        self.addFunction(ConnMailFunction)


class ConnMailFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        logging.debug('__init__() called BinanceOHLCFUnction')

    def execute(self, record):

        # recipient, sender, credentials, server_url, server_port,
        # input_opt_index, input_opt_data, pass_input, message_state, log_state

        recipient, sender, credentials, server_url, server_port, \
                input_opt_index, input_opt_data, pass_input, message_state, \
                log_state = self.config

       

        log_txt = '{BINANCE ORDER}          '
        result = Record(self.getPos(), (self.row +1, self.column), order,
                 log=log_state, log_txt=log_txt)

        return result
