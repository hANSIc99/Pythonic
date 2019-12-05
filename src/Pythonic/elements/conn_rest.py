from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QCheckBox
from PyQt5.QtCore import QCoreApplication as QC
import logging
from Pythonic.elementeditor import ElementEditor
from Pythonic.elementmaster import ElementMaster
from Pythonic.elements.conn_rest_func import ConnRESTFunction

class ConnREST(ElementMaster):

    pixmap_path = 'images/ConnREST.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        # pass_input, url, log_state

        pass_input  = False
        url         = None
        log_state   = False

        self.config = pass_input, url, log_state

        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('ConnREST::__init__() called at row {}, column {}'.format(row, column))
        self.addFunction(ConnRESTFunction)

    def __setstate__(self, state):
        logging.debug('ConnREST::__setstate__() called')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(ConnRESTFunction)

    def __getstate__(self):
        logging.debug('ConnREST::__getstate__() called')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('ConnREST::openEditor() called')

    def edit(self):

        logging.debug('ConnREST::edit()')
        
        


        self.conn_rest_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

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
        self.conn_mail_edit.setWindowTitle(QC.translate('', 'REST (GET)'))

        # signals and slots
        self.confirm_button.clicked.connect(self.conn_mail_edit.closeEvent)
        self.conn_mail_edit.window_closed.connect(self.edit_done)
        self.pass_input_check.stateChanged.connect(self.toggle_url_input)

        # load config
        self.loadLastConfig()

        self.conn_rest_layout.addWidget(self.pass_input_line)
        self.conn_rest_layout.addWidget(self.url_address_txt)
        self.conn_rest_layout.addWidget(self.url_address_input)
        self.conn_rest_layout.addWidget(self.help_text_1)
        self.conn_rest_layout.addWidget(self.log_line)
        self.conn_rest_layout.addWidget(self.confirm_button)
        self.conn_mail_edit.setLayout(self.conn_rest_layout)
        self.conn_mail_edit.show()

    def loadLastConfig(self):

        logging.debug('ConnREST::loadLastConfig() called')
        # pass_input, url, log_state
        pass_input, url, log_state = self.config

        self.pass_input_check.setChecked(pass_input)        
        self.log_checkbox.setChecked(log_state)

        if url:
            self.url_address_input.setText(url)

        

    def toggle_url_input(self, event):

        logging.debug('ConnREST::toggle_url_input() called')
        if event == 0:
            self.url_address_input.setDisabled(False)
        else:
            self.url_address_input.setDisabled(True)



    def edit_done(self):

        logging.debug('ConnREST::edit_done() called')

        # pass_input, url, log_state

        pass_input  = self.pass_input_check.isChecked()
        url         = self.url_address_input.text()
        log_state   = self.log_checkbox.isChecked()

        self.config = pass_input, url, log_state
        logging.debug('########CONFIG: {}'.format(self.config))

        self.addFunction(ConnRESTFunction)
