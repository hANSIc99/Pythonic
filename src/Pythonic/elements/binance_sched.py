from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor, QIntValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox
from elementeditor import ElementEditor
from PyQt5.QtCore import QCoreApplication as QC
from pythonic_binance.client import Client
from time import sleep
import os.path, datetime, logging
from Pythonic.record_function import Record, Function
from Pythonic.elementmaster import ElementMaster


ohlc_steps = { '1m' : 1, '3m' : 3, '5m' : 5, '15m' : 15, '30m' : 30, '1h' : 60, '2h' : 120, '4h' : 240, '6h' : 360,
        '8h' : 480, '12h' : 720, '1d' : 1440, '3d' : 4320, '1w' : 10080, '1M' : 40320 }

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
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config, True)
        super().edit_sig.connect(self.edit)
        logging.debug('BinanceSched called at row {}, column {}'.format(row, column))
        self.addFunction(BinanceScheduler)

    def __setstate__(self, state):
        logging.debug('__setstate__() called BinanceSched')
        self.row, self.column, self.config = state
        # interval-str, inteval-index, offset, log-state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config, True)
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


class BinanceScheduler(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        logging.debug('__init__() called BinanceScheduler')

    def execute(self, record):

        interval_str, interval_index, offset, log_state = self.config

        if isinstance(record, tuple) and isinstance(record[0], datetime.datetime):
            
            while record[0] > datetime.datetime.now():
                sleep(1)

            record = record[1]
            target = (self.row + 1, self.column)
            log_txt = '{BINANCE SCHEDULER}      '
            log_output = '>>>EXECUTE<<<'

            result = Record(self.getPos(), target, record, log=log_state, log_txt=log_txt, log_output=log_output)

        else:

            client = Client('', '')

            try:
                binance_time = client.get_server_time()
            except Exception as e:
                log_txt = '{{BINANCE SCHEDULER}}      Exception caught: {}'.format(str(e))
                result = Record(self.getPos(), None, None, log=True, log_txt=log_txt)

            binance_time = binance_time['serverTime']
            binance_time /= 1000
            binance_timestamp = datetime.datetime.fromtimestamp(binance_time)

            offset = datetime.timedelta(seconds=offset)

            ohlc_step = datetime.timedelta(minutes=ohlc_steps[interval_str])

            date = datetime.datetime.now().date()
            # 00:00 o'clock for the actual date
            sync_time = datetime.datetime(date.year, date.month, date.day)

            # while loop leaves when the next ohlc_step target time is found 
            while sync_time < binance_timestamp:
                sync_time += ohlc_step


            sync_time += offset
            countdown = sync_time - datetime.datetime.now()

            target = self.getPos()
            record = (sync_time, record)
            log_txt = '{BINANCE SCHEDULER}      Synchronization successful'
            log_output = 'Execution starts in {}'.format(countdown)

            result = Record(self.getPos(), target, record, log=log_state, log_txt=log_txt, log_output=log_output)

        return result
