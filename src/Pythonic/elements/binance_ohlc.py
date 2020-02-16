from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
        QLabel, QWidget, QComboBox, QCheckBox)
from PyQt5.QtCore import QCoreApplication as QC
import logging
from Pythonic.elementeditor import ElementEditor
from Pythonic.elementmaster import ElementMaster
from Pythonic.elements.binance_ohlc_func import BinanceOHLCFUnction


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

        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('BinanceOHLC called at row {}, column {}'.format(row, column))
        self.addFunction(BinanceOHLCFUnction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called BinanceOHLC')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
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
        self.binance_ohlc_edit.setWindowTitle(QC.translate('', 'Edit OHLC Query'))

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
