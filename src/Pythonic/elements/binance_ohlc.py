from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor, QIntValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox
from PyQt5.QtCore import QCoreApplication as QC
from pythonic_binance.client import Client
from time import sleep
import os.path, datetime, logging
import pandas as pd
from Pythonic.record_function import Record, Function
from Pythonic.elementeditor import ElementEditor
from Pythonic.elementmaster import ElementMaster

ohlc_steps = { '1m' : 1, '3m' : 3, '5m' : 5, '15m' : 15, '30m' : 30, '1h' : 60, '2h' : 120, '4h' : 240, '6h' : 360,
        '8h' : 480, '12h' : 720, '1d' : 1440, '3d' : 4320, '1w' : 10080, '1M' : 40320 }

class BinanceOHLC(ElementMaster):

    pixmap_path = 'images/BinanceOHLC.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        interval_str = '1m'
        interval_index = 0
        log_state = False
        symbol_txt = None


        # interval-str, inteval-index, symbol_txt, log-state
        self.config = (interval_str, interval_index, symbol_txt, log_state)

        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('BinanceOHLC called at row {}, column {}'.format(row, column))
        self.addFunction(BinanceOHLCFUnction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called BinanceOHLC')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(BinanceOHLCFUnction)

    def __getstate__(self):
        logging.debug('__getstate__() called BinanceOHLC')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called BinanceOHLC')

    def edit(self):

        logging.debug('edit() called BinanceOHLC')

        # interval-str, inteval-index, symbol_txt, log-state
        interval_str, interval_index, symbol_txt, log_state = self.config

        self.binance_ohlc_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.interval_txt = QLabel()
        self.interval_txt.setText(QC.translate('', 'Choose the OHLC interval'))

        # https://github.com/sammchardy/python-binance/blob/master/binance/client.py
        self.selectInterval = QComboBox()
        self.selectInterval.addItem(QC.translate('', '1 Minute'), QVariant('1m'))
        self.selectInterval.addItem(QC.translate('', '3 Minutes'), QVariant('3m'))
        self.selectInterval.addItem(QC.translate('', '5 Minutes'), QVariant('5m'))
        self.selectInterval.addItem(QC.translate('', '15 Minutes'), QVariant('15m'))
        self.selectInterval.addItem(QC.translate('', '30 Minutes'), QVariant('30m'))
        self.selectInterval.addItem(QC.translate('', '1 Hour'), QVariant('1h'))
        self.selectInterval.addItem(QC.translate('', '2 Hours'), QVariant('2h'))
        self.selectInterval.addItem(QC.translate('', '4 Hours'), QVariant('4h'))
        self.selectInterval.addItem(QC.translate('', '6 Hours'), QVariant('6h'))
        self.selectInterval.addItem(QC.translate('', '8 Hours'), QVariant('8h'))
        self.selectInterval.addItem(QC.translate('', '12 Hours'), QVariant('12h'))
        self.selectInterval.addItem(QC.translate('', '1 Day'), QVariant('1d'))
        self.selectInterval.setCurrentIndex(interval_index)


        self.symbol_txt = QLabel()
        self.symbol_txt.setText(QC.translate('', 'Enter currency pair'))

        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText(QC.translate('', 'e.g. "XMRBTC"'))

        if symbol_txt:
            self.symbol_input.setText(symbol_txt)

        self.help_txt = QWidget()
        self.help_txt_layout = QVBoxLayout(self.help_txt)

        self.help_txt_1 = QLabel()
        self.help_txt_1.setText(QC.translate('', 'Outputs a Pandas dataframe in the following format:')) 

        self.help_txt_2 = QLabel()
        self.help_txt_2.setText('\r\n')

        self.help_txt_3 = QLabel()
        self.help_txt_3.setText(QC.translate('','open_time [Unix, 10 digits], open, high, low, close,\r\nvolume, close_time [Unix, 10 digits], quote_assetv,\r\n' \
            'trades, taker_b_asset_v, taker_b_asset_v, datetime'))

        self.help_txt_layout.addWidget(self.help_txt_1)
        self.help_txt_layout.addWidget(self.help_txt_2)
        self.help_txt_layout.addWidget(self.help_txt_3)


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


        self.binance_ohlc_edit = ElementEditor(self)
        self.binance_ohlc_edit.setWindowTitle(QC.translate('', 'Edit OHLC query'))

        # signals and slots
        self.confirm_button.clicked.connect(self.binance_ohlc_edit.closeEvent)
        self.binance_ohlc_edit.window_closed.connect(self.edit_done)

        self.binance_ohlc_layout.addWidget(self.interval_txt)
        self.binance_ohlc_layout.addWidget(self.selectInterval)
        self.binance_ohlc_layout.addWidget(self.symbol_txt)
        self.binance_ohlc_layout.addWidget(self.symbol_input)
        self.binance_ohlc_layout.addWidget(self.log_line)
        self.binance_ohlc_layout.addStretch(1)
        self.binance_ohlc_layout.addWidget(self.help_txt)
        self.binance_ohlc_layout.addWidget(self.confirm_button)
        self.binance_ohlc_edit.setLayout(self.binance_ohlc_layout)
        self.binance_ohlc_edit.show()

    def edit_done(self):

        logging.debug('edit_done() called BinanceOHLC')

        if self.symbol_input.text() == '':
            symbol_txt = None
        else:
            symbol_txt = self.symbol_input.text()
       
        interval_str    = self.selectInterval.currentData()
        interval_index  = self.selectInterval.currentIndex()
        log_state       = self.log_checkbox.isChecked()

        # interval-str, inteval-index, symbol_txt, log-state
        self.config = (interval_str, interval_index, symbol_txt, log_state)

        self.addFunction(BinanceOHLCFUnction)


class BinanceOHLCFUnction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        logging.debug('__init__() called BinanceOHLCFUnction')

    def execute(self, record):

        
        interval_str, inteval_index, symbol_txt, log_state = self.config

        client = Client('', '')
        try:
            record = client.get_klines(symbol=symbol_txt, interval=interval_str)
        except Exception as e:
            log_txt = '{{BINANCE SCHEDULER}}      Exception caught: {}'.format(str(e))
            result = Record(self.getPos(), None, None, log=log_state, log_txt=log_txt)
            return result

        myList  = []
        item    = []


        try:
            for item in record:
                n_item = []
                int_ts = int(item[0]/1000)
                # nur neue timestamps anhängen

                n_item.append(int_ts)            # open time
                n_item.append(float(item[1]))    # open
                n_item.append(float(item[2]))    # high
                n_item.append(float(item[3]))    # low 
                n_item.append(float(item[4]))    # close 
                n_item.append(float(item[5]))    # volume 
                n_item.append(int(item[6]/1000)) # close_time 
                n_item.append(float(item[7]))    # quote_assetv 
                n_item.append(int(item[8]))      # trades 
                n_item.append(float(item[9]))    # taker_b_asset_v
                n_item.append(float(item[10]))   # taker_b_quote_v
                n_item.append(datetime.datetime.fromtimestamp(n_item[0]))
                myList.append(n_item)
        except:
            logging.error('Data cant be read!')
            log_txt = '{{BINANCE SCHEDULER}}      Exception caught: {}'.format(str(e))
            result = Record(self.getPos(), None, None, log=log_state, log_txt=log_txt)
            return result

        new_ohlc = pd.DataFrame(myList, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
            'quote_assetv', 'trades', 'taker_b_asset_v', 'taker_b_quote_v', 'datetime'])

        log_txt = '{BINANCE SCHEDULER}      Query successful'
        log_output = 'Received {} records'.format(len(record))
        result = Record(self.getPos(), (self.row +1, self.column), new_ohlc, log=log_state, log_txt=log_txt, log_output=log_output)

        return result

