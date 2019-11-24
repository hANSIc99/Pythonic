from PyQt5.QtGui import  QIntValidator
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel,
        QTextEdit, QWidget, QComboBox, QCheckBox)
from PyQt5.QtCore import QCoreApplication as QC
import logging
from Pythonic.elementeditor import ElementEditor
from Pythonic.elementmaster import ElementMaster
from Pythonic.elements.conn_mail_func import ConnMailFunction

class ConnMail(ElementMaster):

    pixmap_path = 'images/ConnMail.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        recipient       = None
        sender          = None
        password        = None
        server_url      = None
        server_port     = '465'
        subject         = None
        input_opt_index = 0
        input_opt_data  = None
        filename        = None
        pass_input      = False
        message_state   = False
        message_txt     = None
        log_state       = False

        # recipient, sender, password, server_url, server_port, subject
        # input_opt_index, input_opt_data, filename, pass_input, message_state, message_txt, log_state
        self.config = (recipient, sender, password, server_url, server_port, subject,
                input_opt_index, input_opt_data, filename, pass_input, message_state, message_txt, log_state)

        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('ConnMail::__init__() called at row {}, column {}'.format(row, column))
        self.addFunction(ConnMailFunction)

    def __setstate__(self, state):
        logging.debug('ConnMail::__setstate__() called')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(ConnMailFunction)

    def __getstate__(self):
        logging.debug('ConnMail__getstate__() called')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('ConnMail::openEditor() called')

    def edit(self):

        logging.debug('ConnMail::edit()')
        
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

        self.password_txt = QLabel()
        self.password_txt.setText(QC.translate('', 'Enter password:'))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

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
        self.message_box_txt.setText(QC.translate('', 'Activate user defined message text?'))
        self.message_box_checkbox = QCheckBox()
        self.message_box_line_layout = QHBoxLayout(self.message_box_line)
        self.message_box_line_layout.addWidget(self.message_box_txt)
        self.message_box_line_layout.addWidget(self.message_box_checkbox)
        self.message_box_line_layout = QHBoxLayout(self.message_box_line)

        self.message_txt_input = QTextEdit()


        self.input_option_line = QWidget()
        self.input_option_txt = QLabel()
        self.input_option_txt.setText(QC.translate('', 'Use input as:'))
        self.input_options = QComboBox()
        self.input_options.addItem(QC.translate('', 'None'))
        self.input_options.addItem(QC.translate('', 'Message text'))
        self.input_options.addItem(QC.translate('', 'Attachment (String)'))
        self.input_options.addItem(QC.translate('', 'Attachment (Pickle)'))
        self.input_option_line_layout = QHBoxLayout(self.input_option_line)
        self.input_option_line_layout.addWidget(self.input_option_txt)
        self.input_option_line_layout.addWidget(self.input_options)

        self.filename_input_line = QWidget()
        self.filename_input_line_layout = QHBoxLayout(self.filename_input_line)
        self.filename_input_txt = QLabel()
        self.filename_input_txt.setText(QC.translate('', 'Filename:'))
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText(QC.translate('', 'filename.txt'))
        self.filename_input_line_layout.addWidget(self.filename_input_txt)
        self.filename_input_line_layout.addWidget(self.filename_input)


        self.input_params_1 = QLabel()
        self.input_params_1.setText(QC.translate('', 'Note: Input configuration dict has priority'))
        self.input_params_2 = QLabel()
        self.input_params_2.setText(
                '{\'subject\' : \'Hello\', \'message\' : \'World!\'}')


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

        
        self.conn_mail_edit = ElementEditor(self)
        self.conn_mail_edit.setWindowTitle(QC.translate('', 'Send E-Mail'))
        #self.conn_mail_edit.setMinimumSize(240, 330)

        # signals and slots
        self.confirm_button.clicked.connect(self.conn_mail_edit.closeEvent)
        self.conn_mail_edit.window_closed.connect(self.edit_done)
        self.message_box_checkbox.stateChanged.connect(self.toggle_message_box)
        self.input_options.currentIndexChanged.connect(self.indexChanged)
        # load existing config
        self.loadLastConfig() 

        self.conn_mail_layout.addWidget(self.recipient_address_txt)
        self.conn_mail_layout.addWidget(self.recipient_address_input)
        self.conn_mail_layout.addWidget(self.sender_address_txt)
        self.conn_mail_layout.addWidget(self.sender_address_input)
        self.conn_mail_layout.addWidget(self.password_txt)
        self.conn_mail_layout.addWidget(self.password_input)
        self.conn_mail_layout.addWidget(self.server_txt)
        self.conn_mail_layout.addWidget(self.server_input_line)
        self.conn_mail_layout.addWidget(self.subject_txt)
        self.conn_mail_layout.addWidget(self.subject_input)
        self.conn_mail_layout.addWidget(self.message_box_line)
        self.conn_mail_layout.addWidget(self.message_txt_input)
        self.conn_mail_layout.addWidget(self.input_option_line)
        self.conn_mail_layout.addWidget(self.filename_input_line)
        self.conn_mail_layout.addWidget(self.input_params_1)
        self.conn_mail_layout.addWidget(self.input_params_2)
        self.conn_mail_layout.addWidget(self.pass_input_line)

        self.conn_mail_layout.addWidget(self.help_txt)
        self.conn_mail_layout.addWidget(self.log_line)
        self.conn_mail_layout.addWidget(self.confirm_button)
        self.conn_mail_edit.setLayout(self.conn_mail_layout)
        self.conn_mail_edit.show()
        

    def toggle_message_box(self, event):

        logging.debug('ConnMail::toggle_message_box() called')
        if event == 0:
            self.message_txt_input.setDisabled(True)
        else:
            self.message_txt_input.setDisabled(False)

    def indexChanged(self, event):

        current_index = event
        logging.debug('ConnMail::indexChanged() called: {}'.format(event))
        if event == 2 or event == 3:
            self.filename_input_line.setVisible(True)
        else:
            self.filename_input_line.setVisible(False)



    def loadLastConfig(self):

        # recipient, sender, password, server_url, server_port, subject
        # input_opt_index, input_opt_data, filename, pass_input, message_state, log_state

        recipient, sender, password, server_url, server_port, subject, \
                input_opt_index, input_opt_data, filename, pass_input, message_state, \
                message_txt, log_state = self.config

        if message_state:
            self.toggle_message_box(2)
            self.message_box_checkbox.setChecked(True)
        else:
            self.toggle_message_box(0)
            self.message_box_checkbox.setChecked(False)


        if pass_input:
            self.pass_input_check.setChecked(True)
        else:
            self.pass_input_check.setChecked(False)

        if recipient:
            self.recipient_address_input.setText(recipient)

        if sender:
            self.sender_address_input.setText(sender)

        if password:
            self.password_input.setText(password)

        if server_url:
            self.server_url_input.setText(server_url)

        if server_port:
            self.server_port_input.setText(server_port)

        if subject:
            self.subject_input.setText(subject)
        
        if message_txt:
            self.message_txt_input.setPlainText(message_txt)

        if filename:
            self.filename_input.setText(filename)

        if log_state:
            self.log_checkbox.setChecked(True)
        else:
            self.log_checkbox.setChecked(False)

        self.input_options.setCurrentIndex(input_opt_index)
        self.indexChanged(input_opt_index)




    def edit_done(self):

        logging.debug('ConnMail::edit_done() called')

        recipient       = self.recipient_address_input.text()
        sender          = self.sender_address_input.text()
        password        = self.password_input.text() 
        server_url      = self.server_url_input.text()
        server_port     = self.server_port_input.text()
        subject         = self.subject_input.text()
        input_opt_index = self.input_options.currentIndex()
        input_opt_data  = self.input_options.currentData()
        filename        = self.filename_input.text()

        pass_input      = self.pass_input_check.isChecked()
        message_state   = self.message_box_checkbox.isChecked()   
        log_state       = self.log_checkbox.isChecked()

        if self.message_txt_input.toPlainText() == '':
            message_txt = None
        else:
            message_txt = self.message_txt_input.toPlainText()
        # recipient, sender, password, server_url, server_port, subject
        # input_opt_index, input_opt_data, filename, pass_input, message_state, message_txt, log_state
        self.config = (recipient, sender, password, server_url, server_port, subject,
                input_opt_index, input_opt_data, filename, pass_input, message_state, message_txt, log_state)

        self.addFunction(ConnMailFunction)
