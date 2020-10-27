from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
        QLabel, QWidget, QComboBox, QCheckBox)
from PyQt5.QtCore import QCoreApplication as QC
import logging
from Pythonic.elementeditor import ElementEditor
from Pythonic.elementmaster import ElementMaster
import ccxt, inspect
#from Pythonic.elements.binance_ohlc_func import BinanceOHLCFUnction


class CCXT(ElementMaster):

    pixmap_path = 'images/CCXT.png'
    child_pos = (True, False)

    current_exchange    = 'kraken'
    current_method      = ''

    def __init__(self, row, column):
        self.row = row
        self.column = column

        interval_str = '1m'
        interval_index = 0
        log_state = False
        symbol_txt = None

        # interval-str, inteval-index, symbol_txt, log-state
        self.config = (interval_str, interval_index, symbol_txt, log_state)
        #new
        # exchange_index,

        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('CCXT called at row {}, column {}'.format(row, column))
        #self.addFunction(BinanceOHLCFUnction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called CCXT')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(BinanceOHLCFUnction)

    def __getstate__(self):
        logging.debug('__getstate__() called CCXT')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called CCXT')

    def edit(self):

        logging.debug('edit() called CCXT')

        # interval-str, inteval-index, symbol_txt, log-state
        interval_str, interval_index, symbol_txt, log_state = self.config

        self.ccxt_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.exchange_txt = QLabel()
        self.exchange_txt.setText(QC.translate('', 'Choose Exchange'))

        # https://github.com/sammchardy/python-binance/blob/master/binance/client.py
        self.selectExchange = QComboBox()

        for exchange_id in ccxt.exchanges:
            try:
                exchange = getattr(ccxt, exchange_id)()
                self.selectExchange.addItem(exchange.name, QVariant(exchange_id))
            except Exception as e:
                print(e)

        self.selectExchange.setCurrentIndex(interval_index)

        self.current_exchange = getattr(ccxt, self.selectExchange.currentData())()

        self.pub_key_txt = QLabel()
        self.pub_key_txt.setText(QC.translate('', 'Enter API key:'))
        self.pub_key_input = QLineEdit()

        self.prv_key_txt = QLabel()
        self.prv_key_txt.setText(QC.translate('', 'Enter secret key:'))
        self.prv_key_input = QLineEdit()

        # List all available functions

        self.method_txt = QLabel()
        self.method_txt.setText(QC.translate('', 'Select method'))

        self.selectMethod = QComboBox()
        self.updateMethods()

        self.method_params = QWidget()
        self.method_params_layout = QVBoxLayout(self.method_params)



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


        self.ccxt_edit = ElementEditor(self)
        self.ccxt_edit.setWindowTitle(QC.translate('', 'CCXT'))

        # signals and slots
        self.confirm_button.clicked.connect(self.ccxt_edit.closeEvent)
        self.ccxt_edit.window_closed.connect(self.edit_done)
        self.selectExchange.currentIndexChanged.connect(self.exchangeChanged)
        self.selectMethod.currentIndexChanged.connect(self.methodChanged)

        self.ccxt_layout.addWidget(self.exchange_txt)
        self.ccxt_layout.addWidget(self.selectExchange)  
        self.ccxt_layout.addWidget(self.pub_key_txt)
        self.ccxt_layout.addWidget(self.pub_key_input)
        self.ccxt_layout.addWidget(self.prv_key_txt)
        self.ccxt_layout.addWidget(self.prv_key_input)
        self.ccxt_layout.addWidget(self.selectMethod)
        self.ccxt_layout.addWidget(self.method_params)
        self.ccxt_layout.addWidget(self.log_line)
        self.ccxt_layout.addStretch(1)
        
        self.ccxt_layout.addWidget(self.confirm_button)
        self.ccxt_edit.setLayout(self.ccxt_layout)
        self.ccxt_edit.show()

    def exchangeChanged(self, event):
        
        logging.debug('CCXT::exchangeChanged() called {}'.format(event))
        
        self.current_exchange = getattr(ccxt, self.selectExchange.currentData())()
        self.updateMethods()

    def methodChanged(self, event):
        
        logging.debug('updateSignature() called CCXT')
         
        self.current_method = getattr(self.current_exchange, self.selectMethod.currentData())
        signature = inspect.signature(self.current_method)
        print('test')

    def newmethod584(self):
        return self.current_method

    def updateMethods(self):

        logging.debug('CCXT::updateMethods() called')
        self.selectMethod.clear()

        for method in inspect.getmembers(self.current_exchange, predicate=inspect.ismethod):
            if method[0][:2] != '__' :
                # mit getattr lässt sich die methode dann wieder aufrufen
                
                self.selectMethod.addItem(method[0], QVariant(method[0]))
        self.selectMethod.show()

    def updateSignature(self):

        #signature = inspect.signature()
        logging.debug('updateSignature() called CCXT')


  

    def edit_done(self):

        logging.debug('edit_done() called CCXT')
        """
        if self.symbol_input.text() == '':
            symbol_txt = None
        else:
            symbol_txt = self.symbol_input.text()
       
        interval_str    = self.selectInterval.currentData()
        interval_index  = self.selectInterval.currentIndex()
        log_state       = self.log_checkbox.isChecked()
        """
        # interval-str, inteval-index, symbol_txt, log-state
        #self.config = (interval_str, interval_index, symbol_txt, log_state)

        #self.addFunction(BinanceOHLCFUnction)
