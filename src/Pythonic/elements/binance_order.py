from elementmaster import ElementMaster
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor, QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox, QStackedWidget
from elementeditor import ElementEditor
from PyQt5.QtCore import QCoreApplication as QC
import logging
from time import sleep
import os.path, datetime
from record_function import Record, Function
from elementmaster import alphabet
from binance.client import Client
import pandas as pd


class BinanceOrder(ElementMaster):

    pixmap_path = 'images/BinanceOrder.png'
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
        self.addFunction(BinanceOrderFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called BinanceOrder')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(BinanceOrderFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called BinanceOrder')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called BinanceOrder')

    def edit(self):

        logging.debug('edit() called BinanceOrder')

        pub_key, prv_key, side_index, side_txt, symbol_txt, quantity, \
                order_index, order_string, order_config, log_state = self.config

        self.binance_order_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.pub_key_txt = QLabel()
        self.pub_key_txt.setText(QC.translate('', 'Enter API key:'))
        self.pub_key_input = QLineEdit()

        self.prv_key_txt = QLabel()
        self.prv_key_txt.setText(QC.translate('', 'Enter secret key:'))
        self.prv_key_input = QLineEdit()



        self.symbol_txt = QLabel()
        self.symbol_txt.setText(QC.translate('', 'Enter currency pair'))

        self.order_data_line = QWidget()
        self.order_data_layout = QHBoxLayout(self.order_data_line)

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

        self.help_txt = QLabel()
        self.help_txt.setText(QC.translate('', 'Attention: Use a dot (".") as decimal seperator!'))

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
        self.selectOrder.currentIndexChanged.connect(self.indexChanged)

        self.binance_order_layout.addWidget(self.pub_key_txt)
        self.binance_order_layout.addWidget(self.pub_key_input)
        self.binance_order_layout.addWidget(self.prv_key_txt)
        self.binance_order_layout.addWidget(self.prv_key_input)
        self.binance_order_layout.addWidget(self.symbol_txt)
        self.binance_order_layout.addWidget(self.order_data_line)
        self.binance_order_layout.addWidget(self.quantity_txt)
        self.binance_order_layout.addWidget(self.quantity_input)
        self.binance_order_layout.addWidget(self.selectOrder)
        self.binance_order_layout.addStretch(1)
        self.binance_order_layout.addWidget(self.order_box)
        self.binance_order_layout.addWidget(self.help_txt)
        self.binance_order_layout.addWidget(self.log_line)
        self.binance_order_layout.addWidget(self.confirm_button)
        self.binance_order_edit.setLayout(self.binance_order_layout)
        self.binance_order_edit.show()

    def limitOrder(self):

        logging.debug('limitOrder() called')

        self.limit_input = QWidget()
        self.limit_layout = QVBoxLayout(self.limit_input)

        self.limit_time_in_force_txt = QLabel()
        self.limit_time_in_force_txt.setText(QC.translate('', 'Time in force:'))

        self.limit_time_in_force_input = QComboBox()
        self.limit_time_in_force_input.addItem(QC.translate('', 'Good til canceled'), QVariant('GTC'))
        self.limit_time_in_force_input.addItem(QC.translate('', 'Immediate or Cancel'), QVariant('IOC'))
        self.limit_time_in_force_input.addItem(QC.translate('', 'Fill or Kill'), QVariant('FOK'))

        self.limit_price_txt = QLabel()
        self.limit_price_txt.setText(QC.translate('', 'Limit price:'))

        self.limit_price_input = QLineEdit()
        self.limit_price_input.setValidator(QDoubleValidator(999999, -999999, 8))

        self.limit_layout.addWidget(self.limit_time_in_force_txt)
        self.limit_layout.addWidget(self.limit_time_in_force_input)
        self.limit_layout.addWidget(self.limit_price_txt)
        self.limit_layout.addWidget(self.limit_price_input)

        self.order_box.addWidget(self.limit_input)

    def stopLoss(self):

        logging.debug('stopLoss() called')

        self.stop_loss_input = QWidget()
        self.stop_loss_layout = QVBoxLayout(self.stop_loss_input)

        self.stop_loss_price_txt = QLabel()
        self.stop_loss_price_txt.setText(QC.translate('', 'Stop price:'))

        self.stop_loss_price_input = QLineEdit()
        self.stop_loss_price_input.setValidator(QDoubleValidator(999999, -999999, 8))

        self.stop_loss_layout.addWidget(self.stop_loss_price_txt)
        self.stop_loss_layout.addWidget(self.stop_loss_price_input)
        self.stop_loss_layout.addStretch(1)

        self.order_box.addWidget(self.stop_loss_input)

    def stopLossLimit(self):

        logging.debug('stopLossLimit() called')

        self.stop_loss_limit_input = QWidget()
        self.stop_loss_limit_layout = QVBoxLayout(self.stop_loss_limit_input)

        self.stop_loss_limit_time_in_force_txt = QLabel()
        self.stop_loss_limit_time_in_force_txt.setText(QC.translate('', 'Time in force:'))

        self.stop_loss_limit_time_in_force_input = QComboBox()
        self.stop_loss_limit_time_in_force_input.addItem(QC.translate('', 'Good til canceled'), QVariant('GTC'))
        self.stop_loss_limit_time_in_force_input.addItem(QC.translate('', 'Immediate or Cancel'), QVariant('IOC'))
        self.stop_loss_limit_time_in_force_input.addItem(QC.translate('', 'Fill or Kill'), QVariant('FOK'))


        self.stop_loss_limit_price_txt = QLabel()
        self.stop_loss_limit_price_txt.setText(QC.translate('', 'Price:'))

        self.stop_loss_limit_price_input = QLineEdit()
        self.stop_loss_limit_price_input.setValidator(QDoubleValidator(999999, -999999, 8))


        self.stop_loss_limit_stop_price_txt = QLabel()
        self.stop_loss_limit_stop_price_txt.setText(QC.translate('', 'Stop price:'))

        self.stop_loss_limit_stop_price_input = QLineEdit()
        self.stop_loss_limit_stop_price_input.setValidator(QDoubleValidator(999999, -999999, 8))

        self.stop_loss_limit_layout.addWidget(self.stop_loss_limit_time_in_force_txt)
        self.stop_loss_limit_layout.addWidget(self.stop_loss_limit_time_in_force_input)
        self.stop_loss_limit_layout.addWidget(self.stop_loss_limit_price_txt)
        self.stop_loss_limit_layout.addWidget(self.stop_loss_limit_price_input)
        self.stop_loss_limit_layout.addWidget(self.stop_loss_limit_stop_price_txt)
        self.stop_loss_limit_layout.addWidget(self.stop_loss_limit_stop_price_input)

        self.order_box.addWidget(self.stop_loss_limit_input)

    def takeProfit(self):

        logging.debug('takeProfit() called')

        self.take_profit_input = QWidget()
        self.take_profit_layout = QVBoxLayout(self.take_profit_input)

        self.take_profit_stop_price = QLabel()
        self.take_profit_stop_price.setText(QC.translate('', 'Stop price:'))

        self.take_profit_stop_price_input = QLineEdit()
        self.take_profit_stop_price_input.setValidator(QDoubleValidator(999999, -999999, 8))

        self.take_profit_layout.addWidget(self.take_profit_stop_price)
        self.take_profit_layout.addWidget(self.take_profit_stop_price_input)
        self.take_profit_layout.addStretch(1)

        self.order_box.addWidget(self.take_profit_input)

    def takeProfitLimit(self):

        logging.debug('takeProfitLimit() called')

        self.take_profit_limit_input = QWidget()
        self.take_profit_limit_layout = QVBoxLayout(self.take_profit_limit_input)

        self.take_profit_limit_time_in_force_txt = QLabel()
        self.take_profit_limit_time_in_force_txt.setText(QC.translate('', 'Time in force:'))

        self.take_profit_limit_time_in_force_input = QComboBox()
        self.take_profit_limit_time_in_force_input.addItem(QC.translate('', 'Good til canceled'), QVariant('GTC'))
        self.take_profit_limit_time_in_force_input.addItem(QC.translate('', 'Immediate or Cancel'), QVariant('IOC'))
        self.take_profit_limit_time_in_force_input.addItem(QC.translate('', 'Fill or Kill'), QVariant('FOK'))

        self.take_profit_limit_price = QLabel()
        self.take_profit_limit_price.setText(QC.translate('', 'Price:'))

        self.take_profit_limit_price_input = QLineEdit()
        self.take_profit_limit_price_input.setValidator(QDoubleValidator(999999, -999999, 8))


        self.take_profit_limit_stop_price = QLabel()
        self.take_profit_limit_stop_price.setText(QC.translate('', 'Stop price:'))

        self.take_profit_limit_stop_price_input = QLineEdit()
        self.take_profit_limit_stop_price_input.setValidator(QDoubleValidator(999999, -999999, 8))

        self.take_profit_limit_layout.addWidget(self.take_profit_limit_time_in_force_txt)
        self.take_profit_limit_layout.addWidget(self.take_profit_limit_time_in_force_input)
        self.take_profit_limit_layout.addWidget(self.take_profit_limit_price)
        self.take_profit_limit_layout.addWidget(self.take_profit_limit_price_input)
        self.take_profit_limit_layout.addWidget(self.take_profit_limit_stop_price)
        self.take_profit_limit_layout.addWidget(self.take_profit_limit_stop_price_input)

        self.order_box.addWidget(self.take_profit_limit_input)

    def marketOrder(self):

        logging.debug('marketOrder() called')

        self.market_input = QWidget()
        self.market_layout = QHBoxLayout(self.market_input)

        self.order_box.addWidget(self.market_input)

    def limitMaker(self):

        logging.debug('limitMaker() called')

        self.limit_maker_input = QWidget()
        self.limit_maker_layout = QHBoxLayout(self.limit_maker_input)

        self.order_box.addWidget(self.limit_maker_input)


    def testOrder(self):

        logging.debug('testOrder() called')

        self.test_input = QWidget()
        self.test_layout = QHBoxLayout(self.test_input)

        self.test_order_txt = QLabel()
        self.test_order_txt.setText(QC.translate('', 'Test order without effect.'))

        self.test_layout.addWidget(self.test_order_txt)
        self.order_box.addWidget(self.test_input)

    def indexChanged(self, event):

        current_index = event
        logging.debug('indexChanged() called {}'.format(current_index))
        self.order_box.setCurrentIndex(current_index)

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

        logging.debug('edit_done() called BinanceOrder')

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

        self.config = (pub_key, prv_key, side_index, side_txt, symbol_txt, quantity, order_index, order_string, order_config, log_state)

        self.addFunction(BinanceOrderFunction)


class BinanceOrderFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        logging.debug('__init__() called BinanceOHLCFUnction')

    def execute(self, record):

        
        pub_key, prv_key, side_index, side_txt, symbol_txt, quantity, order_index, order_string, order_config, log_state = self.config

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
        result = Record(self.getPos(), (self.row +1, self.column), order, log=log_state, log_txt=log_txt)

        return result
