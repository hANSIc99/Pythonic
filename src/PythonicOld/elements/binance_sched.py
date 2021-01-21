from PyQt5.QtCore import QVariant
from PyQt5.QtGui import  QIntValidator
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
        QLabel, QWidget, QComboBox, QCheckBox)
from PyQt5.QtCore import QCoreApplication as QC
import logging
from Pythonic.elementeditor import ElementEditor
from Pythonic.elementmaster import ElementMaster
from Pythonic.elements.binance_sched_func import BinanceScheduler


class BinanceSched(ElementMaster):

    pixmap_path = 'images/BinanceSched.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        interval_str = '1m'
        interval_index = 0
        offset  = 0
        log_state = False

        # interval-str, inteval-index, offset, log-state
        self.config = (interval_str, interval_index, offset, log_state)

        # self_sync = True (last True)
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config, True)
        super().edit_sig.connect(self.edit)
        logging.debug('BinanceSched called at row {}, column {}'.format(row, column))
        self.addFunction(BinanceScheduler)

    def __setstate__(self, state):
        logging.debug('__setstate__() called BinanceSched')
        self.row, self.column, self.config = state
        # interval-str, inteval-index, offset, log-state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config, True)
        super().edit_sig.connect(self.edit)
        self.addFunction(BinanceScheduler)

    def __getstate__(self):
        logging.debug('__getstate__() called BinanceSched')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called BinanceSched')

    def edit(self):

        logging.debug('edit() called BinanceSched')

        interval_str, interval_index, offset, log_state = self.config

        self.binance_sched_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.interval_txt = QLabel()
        self.interval_txt.setText(QC.translate('', 'Choose the scheduler interval'))

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

        self.offset_txt = QLabel()
        self.offset_txt.setText(QC.translate('',
            'Enter time offset [s] (default: 0; range: -999s to + 999s)'))

        self.offset_input = QLineEdit()
        self.offset_input.setValidator(QIntValidator(-999, 999))
        self.offset_input.setText(str(offset))

        self.help_text = QWidget()
        self.help_text_layout = QVBoxLayout(self.help_text)

        self.help_text_1 = QLabel()
        self.help_text_1.setText(QC.translate('',
            'Synchronize with Binance and execute subsequent modules')) 

        self.help_text_2 = QLabel()
        self.help_text_2.setText(QC.translate('', 'after expiration of the selected interval.'))

        self.help_text_layout.addWidget(self.help_text_1)
        self.help_text_layout.addWidget(self.help_text_2)

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


        self.binance_sched_edit = ElementEditor(self)
        self.binance_sched_edit.setWindowTitle(QC.translate('', 'Edit Binance Scheduler'))

        # signals and slots
        self.confirm_button.clicked.connect(self.binance_sched_edit.closeEvent)
        self.binance_sched_edit.window_closed.connect(self.edit_done)


        self.binance_sched_layout.addWidget(self.interval_txt)
        self.binance_sched_layout.addWidget(self.selectInterval)
        self.binance_sched_layout.addWidget(self.offset_txt)
        self.binance_sched_layout.addWidget(self.offset_input)
        self.binance_sched_layout.addWidget(self.log_line)
        self.binance_sched_layout.addWidget(self.help_text)
        self.binance_sched_layout.addStretch(1)
        self.binance_sched_layout.addWidget(self.confirm_button)
        self.binance_sched_edit.setLayout(self.binance_sched_layout)
        self.binance_sched_edit.show()

    def edit_done(self):

        logging.debug('edit_done() called BinanceSched')
        
        interval_str    = self.selectInterval.currentData()
        interval_index  = self.selectInterval.currentIndex()
        log_state       = self.log_checkbox.isChecked()
        try:
            offset = int(self.offset_input.text())
        except Exception as e:
            offset = 0

        # interval-str, inteval-index, offset, log-state
        self.config = (interval_str, interval_index, offset, log_state)

        self.addFunction(BinanceScheduler)
