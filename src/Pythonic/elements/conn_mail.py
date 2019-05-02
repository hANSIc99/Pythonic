from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
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

        pub_key = None
        prv_key = None
        side_index = 0
        side_txt = 'BUY'
        symbol_txt = None
        quantity = 0.0
        order_index = 0
        order_string = 'MARKET'
        order_config = (0, )
        log_state = False

        self.config = (pub_key, prv_key, side_index, side_txt, symbol_txt, \
                quantity, order_index, order_string, order_config, log_state)

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

        pub_key, prv_key, side_index, side_txt, symbol_txt, quantity, \
                order_index, order_string, order_config, log_state = self.config

        self.binance_order_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.recipient_address_txt = QLabel()
        self.recipient_address_txt.setText(QC.translate('', 'Recipient address:'))
        self.recipient_address_input = QLineEdit()

        self.sender_address_txt = QLabel()
        self.sender_address_txt.setText(QC.translate('', 'Enter sender address:'))
        self.sender_address_input = QLineEdit()

        self.credentials_txt = QLabel()
        self.credentials_txt.setText(QC.translate('', 'Enter credentials:'))
        self.credentials_input = QLineEdit()

        self.subject_txt = QLabel()
        self.subject_txt.setText(QC.translate('', 'Enter subject:'))
        self.subject_input = QLineEdit()

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

        """
        self.symbol_txt = QLabel()
        self.symbol_txt.setText(QC.translate('', 'Enter currency pair'))

        self.order_data_line = QWidget()
        self.order_data_layout = QHBoxLayout(self.order_data_line)
        """

        """ 
        checkbox: Use input in message => wenn aktiviert, wird der input an
        den message text gehangen
        input = attachment
        input = message txt
        checkbox: forward inout to output

        checkbox: activate message text

        in
        attachment
        self.order_side = QComboBox()
        self.order_side.addItem(QC.translate('', 'Buy'), QVariant('BUY'))
        self.order_side.addItem(QC.translate('', 'Sell'), QVariant('SELL'))

        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText(QC.translate('', 'e.g. "XMRBTC"'))

        self.order_data_layout.addWidget(self.order_side)
        self.order_data_layout.addWidget(self.symbol_input)

        self.quantity_txt = QLabel()
        self.quantity_txt.setText(QC.translate('', 'Enter quantity:'))

        if symbol_txt:
            self.symbol_input.setText(symbol_txt)

        self.quantity_input = QLineEdit()
        self.quantity_input.setValidator(QDoubleValidator(999999, -999999, 8))

        self.selectOrder = QComboBox()
        self.selectOrder.addItem(QC.translate('', 'Limit Order'), QVariant('LIMIT'))
        self.selectOrder.addItem(QC.translate('', 'Market Order'), QVariant('MARKET'))
        self.selectOrder.addItem(QC.translate('', 'Stop Loss'), QVariant('STOP_LOSS'))
        self.selectOrder.addItem(QC.translate('', 'Stop Loss Limit'), QVariant('STOP_LOSS_LIMIT'))
        self.selectOrder.addItem(QC.translate('', 'Take Profit'), QVariant('TAKE_PROFIT'))
        self.selectOrder.addItem(QC.translate('', 'Take Profit Limit'), QVariant('TAKE_PROFIT_LIMIT'))
        self.selectOrder.addItem(QC.translate('', 'Limit Maker'), QVariant('LIMIT_MAKER'))
        self.selectOrder.addItem(QC.translate('', 'Test Order'), QVariant('TEST'))

        self.order_box = QStackedWidget()
        self.limitOrder()
        self.marketOrder()
        self.stopLoss()
        self.stopLossLimit()
        self.takeProfit()
        self.takeProfitLimit()
        self.limitMaker()
        self.testOrder()
        self.loadLastConfig()
        """
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


        self.binance_order_edit = ElementEditor(self)
        self.binance_order_edit.setWindowTitle(QC.translate('', 'Place a Order'))
        #self.binance_order_edit.setMinimumSize(240, 330)

        # signals and slots
        self.confirm_button.clicked.connect(self.binance_order_edit.closeEvent)
        self.binance_order_edit.window_closed.connect(self.edit_done)
        #self.selectOrder.currentIndexChanged.connect(self.indexChanged)

        self.binance_order_layout.addWidget(self.recipient_address_txt)
        self.binance_order_layout.addWidget(self.recipient_address_input)
        self.binance_order_layout.addWidget(self.sender_address_txt)
        self.binance_order_layout.addWidget(self.sender_address_input)
        self.binance_order_layout.addWidget(self.credentials_txt)
        self.binance_order_layout.addWidget(self.credentials_input)
        self.binance_order_layout.addWidget(self.message_box_line)
        self.binance_order_layout.addWidget(self.message_txt_input)
        self.binance_order_layout.addWidget(self.input_option_line)
        self.binance_order_layout.addWidget(self.pass_input_line)
        """
        self.binance_order_layout.addWidget(self.quantity_txt)
        self.binance_order_layout.addWidget(self.quantity_input)
        self.binance_order_layout.addWidget(self.selectOrder)
        """
        #self.binance_order_layout.addStretch(1)
        #self.binance_order_layout.addWidget(self.order_box)
        self.binance_order_layout.addWidget(self.help_txt)
        self.binance_order_layout.addWidget(self.log_line)
        self.binance_order_layout.addWidget(self.confirm_button)
        self.binance_order_edit.setLayout(self.binance_order_layout)
        self.binance_order_edit.show()

    def loadLastConfig(self):

        pub_key, prv_key, side_index, side_txt, symbol_txt, quantity, \
                order_index, order_string, order_config, log_state = self.config

        if pub_key != '':
            
            self.pub_key_input.setText(pub_key)

        if prv_key != '':

            self.prv_key_input.setText(prv_key)

        self.quantity_input.setText('{:.8f}'.format(quantity))

        logging.debug('loadLastConfig() called with order_string = {}'.format(order_string))

        self.selectOrder.setCurrentIndex(order_index)
        self.order_box.setCurrentIndex(order_index)
        self.order_side.setCurrentIndex(side_index)

        if order_string == 'LIMIT':
            self.limit_time_in_force_input.setCurrentIndex(order_config[1])
            self.limit_price_input.setText('{:.8f}'.format(order_config[2]))
        elif order_string == 'STOP_LOSS':
            self.stop_loss_price_input.setText('{:.8f}'.format(order_config[0]))
        elif order_string == 'STOP_LOSS_LIMIT':
            self.stop_loss_limit_time_in_force_input.setCurrentIndex(order_config[1])
            self.stop_loss_limit_price_input.setText('{:.8f}'.format(order_config[2]))
            self.stop_loss_limit_stop_price_input.setText('{:.8f}'.format(order_config[3]))
        elif order_string == 'TAKE_PROFIT':
            self.take_profit_stop_price_input.setText('{:.8f}'.format(order_config[0]))
        elif order_string == 'TAKE_PROFIT_LIMIT':
            self.take_profit_limit_time_in_force_input.setCurrentIndex(order_config[1])
            self.take_profit_limit_price_input.setText('{:.8f}'.format(order_config[2]))
            self.take_profit_limit_stop_price_input.setText('{:.8f}'.format(order_config[3]))


    def edit_done(self):

        logging.debug('ConnMail::edit_done() called')

        order_config = None

        if self.selectOrder.currentData() == 'LIMIT':

            tif_string  = self.limit_time_in_force_input.currentData()
            tif_index   = self.limit_time_in_force_input.currentIndex()


            if self.limit_price_input.text() == '':

                limit_price_value = 0.0

            else:

                limit_price_value = float(self.limit_price_input.text())

            logging.warning('limit price: {}'.format(limit_price_value))

            order_config = (tif_string, tif_index, limit_price_value)

        elif self.selectOrder.currentData() == 'STOP_LOSS':

            if self.stop_loss_price_input.text() == '':

                stop_price_value = 0.0

            else:

                stop_price_value = float(self.stop_loss_price_input.text())

            logging.warning('stop price: {}'.format(stop_price_value))

            order_config = (stop_price_value, )

        elif self.selectOrder.currentData() == 'STOP_LOSS_LIMIT':

            tif_string  = self.stop_loss_limit_time_in_force_input.currentData()
            tif_index   = self.stop_loss_limit_time_in_force_input.currentIndex()


            if self.stop_loss_limit_price_input.text() == '':

                limit_price_value = 0.0

            else:

                limit_price_value = float(self.stop_loss_limit_price_input.text())

            if self.stop_loss_limit_stop_price_input.text() == '':

                stop_price_value = 0.0

            else:

                stop_price_value = float(self.stop_loss_limit_stop_price_input.text())


            logging.warning('Limit price: {}'.format(limit_price_value))
            logging.warning('Stop price: {}'.format(stop_price_value))

            order_config = (tif_string, tif_index, limit_price_value, stop_price_value)

        elif self.selectOrder.currentData() == 'TAKE_PROFIT':

            if self.take_profit_stop_price_input.text() == '':

                stop_price_value = 0.0

            else:

                stop_price_value = float(self.take_profit_stop_price_input.text())

            logging.warning('Stop price: {}'.format(stop_price_value))

            order_config = (stop_price_value, )

        elif self.selectOrder.currentData() == 'TAKE_PROFIT_LIMIT':

            tif_string  = self.take_profit_limit_time_in_force_input.currentData()
            tif_index   = self.take_profit_limit_time_in_force_input.currentIndex()


            if self.take_profit_limit_price_input.text() == '':

                limit_price_value = 0.0

            else:

                limit_price_value = float(self.take_profit_limit_price_input.text())

            if self.take_profit_limit_stop_price_input.text() == '':

                stop_price_value = 0.0

            else:

                stop_price_value = float(self.take_profit_limit_stop_price_input.text())
        # TODO: Create Test Order


            logging.warning('Limit price: {}'.format(limit_price_value))
            logging.warning('Stop price: {}'.format(stop_price_value))

            order_config = (tif_string, tif_index, limit_price_value, stop_price_value)


        pub_key     = self.pub_key_input.text()
        prv_key     = self.prv_key_input.text()
        side_index  = self.order_side.currentIndex()
        side_txt    = self.order_side.currentData()
        symbol_txt  = self.symbol_input.text()

        if self.quantity_input.text() == '':
            quantity = 0.0
        else:
            quantity    = float(self.quantity_input.text())

        order_index     = self.selectOrder.currentIndex()
        order_string    = self.selectOrder.currentData()
        log_state       = self.log_checkbox.isChecked()

        self.config = (pub_key, prv_key, side_index, side_txt, symbol_txt,
                quantity, order_index, order_string, order_config, log_state)

        self.addFunction(ConnMailFunction)


class ConnMailFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        logging.debug('__init__() called BinanceOHLCFUnction')

    def execute(self, record):

        
        pub_key, prv_key, side_index, side_txt, symbol_txt, quantity, \
                order_index, order_string, order_config, log_state = self.config

        timeInForce = None
        stopPrice   = None
        price       = None

        client = Client(pub_key, prv_key)

        if order_string == 'MARKET':

            if isinstance(record, dict):
                if 'quantity' in record: 
                    quantity = record['quantity']

            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    )

        elif order_string == 'LIMIT':

            timeInForce = order_config[0]
            price       = '{:.8f}'.format(order_config[2])

            if isinstance(record, dict):
                if 'price' in record: 
                    price = '{:.8f}'.format(record['price'])
                if 'quantity' in record: 
                    quantity = record['quantity']

            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    timeInForce = timeInForce,
                    price       = price,
                    )

        elif order_string == 'STOP_LOSS':

            stopPrice   = '{:.8f}'.format(order_config[0])

            if isinstance(record, dict):
                if 'stopPrice' in record: 
                    stopPrice = '{:.8f}'.format(record['stopPrice'])
                if 'quantity' in record: 
                    quantity = record['quantity']

            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    stopPrice   = stopPrice
                    )

        elif order_string == 'STOP_LOSS_LIMIT':

            timeInForce = order_config[0]
            price       = '{:.8f}'.format(order_config[2])
            stopPrice   = '{:.8f}'.format(order_config[3])

            if isinstance(record, dict):
                if 'price' in record: 
                    price = '{:.8f}'.format(record['price'])
                if 'stopPrice' in record: 
                    stopPrice = '{:.8f}'.format(record['stopPrice'])
                if 'quantity' in record: 
                    quantity = record['quantity']


            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    timeInForce = timeInForce,
                    price       = price,
                    stopPrice   = stopPrice
                    )

        elif order_string == 'TAKE_PROFIT':

            stopPrice   = '{:.8f}'.format(order_config[0])

            if isinstance(record, dict):
                if 'stopPrice' in record: 
                    stopPrice = '{:.8f}'.format(record['stopPrice'])
                if 'quantity' in record: 
                    quantity = record['quantity']



            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    stopPrice   = stopPrice
                    )

        elif order_string == 'TAKE_PROFIT_LIMIT':

            timeInForce = order_config[0]
            price       = '{:.8f}'.format(order_config[2])
            stopPrice   = '{:.8f}'.format(order_config[3])

            if isinstance(record, dict):
                if 'price' in record: 
                    price = '{:.8f}'.format(record['price'])
                if 'stopPrice' in record: 
                    stopPrice = '{:.8f}'.format(record['stopPrice'])
                if 'quantity' in record: 
                    quantity = record['quantity']

            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    timeInForce = timeInForce,
                    price       = price,
                    stopPrice   = stopPrice
                    )

        logging.error('Order: {}'.format(order)) 
        logging.error('symbol = {}'.format(symbol_txt))
        logging.error('side = {}'.format(side_txt))
        logging.error('type = {}'.format(order_string))
        logging.error('quantity = {}'.format(quantity))
        logging.error('timeInForce = {}'.format(timeInForce))
        logging.error('price = {}'.format(price))
        logging.error('stopPrice = {}'.format(stopPrice))

        log_txt = '{BINANCE ORDER}          '
        result = Record(self.getPos(), (self.row +1, self.column), order,
                 log=log_state, log_txt=log_txt)

        return result
