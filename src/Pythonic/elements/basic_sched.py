from elementmaster import ElementMaster
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor, QIntValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox, QStackedWidget
from elementeditor import ElementEditor
from PyQt5.QtCore import QCoreApplication as QC
import logging
from time import sleep
import os.path, datetime
from record_function import Record, Function
from elementmaster import alphabet
from binance.client import Client

ohlc_steps = { '1m' : 1, '3m' : 3, '5m' : 5, '15m' : 15, '30m' : 30, '1h' : 60, '2h' : 120, '4h' : 240, '6h' : 360,
        '8h' : 480, '12h' : 720, '1d' : 1440, '3d' : 4320, '1w' : 10080, '1M' : 40320 }

class ExecSched(ElementMaster):

    pixmap_path = 'images/ExecSched.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        mode_index = 0
        offset  = 0
        log_state = False

        # interval-str, inteval-index, offset, log-state
        self.config = (mode_index, offset, log_state)

        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('ExecSched called at row {}, column {}'.format(row, column))
        self.addFunction(BasicScheduler)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecSched')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(BasicScheduler)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecSched')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called ExecSched')

    def edit(self):

        logging.debug('edit() called ExecSched')

        mode_index, offset, log_state = self.config

        self.basic_sched_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.sched_txt = QLabel()
        self.sched_txt.setText(QC.translate('', 'Choose the scheduler mode'))

        # https://github.com/sammchardy/python-binance/blob/master/binance/client.py
        self.selectMode = QComboBox()
        self.selectMode.addItem(QC.translate('', 'Interval'), QVariant('interval'))
        self.selectMode.addItem(QC.translate('', 'Interval between times'), QVariant('int_time'))
        self.selectMode.addItem(QC.translate('', 'At specific time'), QVariant('time'))
        self.selectMode.setCurrentIndex(mode_index)

        self.options_box = QWidget()
        self.options_box_layout = QVBoxLayout(self.options_box)
        self.interval()
        self.weekdays()
        self.int_time()

        self.offset_txt = QLabel()
        self.offset_txt.setText(QC.translate('', 'Enter time offset [s] (default: 0; range: -999s to + 999s)'))

        self.offset_input = QLineEdit()
        self.offset_input.setValidator(QIntValidator(-999, 999))
        self.offset_input.setText(str(offset))

        self.help_text = QWidget()
        self.help_text_layout = QVBoxLayout(self.help_text)

        self.help_text_1 = QLabel()
        self.help_text_1.setText(QC.translate('', 'Synchronize with Binance and execute subsequent modules')) 

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


        self.basic_sched_edit = ElementEditor(self)
        self.basic_sched_edit.setWindowTitle(QC.translate('', 'Edit Basic Scheduler'))

        # signals and slots
        self.confirm_button.clicked.connect(self.basic_sched_edit.closeEvent)
        self.basic_sched_edit.window_closed.connect(self.edit_done)
        self.selectMode.currentIndexChanged.connect(self.indexChanged)


        self.basic_sched_layout.addWidget(self.sched_txt)
        self.basic_sched_layout.addWidget(self.selectMode)
        self.basic_sched_layout.addWidget(self.options_box)
        
        """
        self.basic_sched_layout.addWidget(self.offset_txt)
        self.basic_sched_layout.addWidget(self.offset_input)
        """
        self.basic_sched_layout.addWidget(self.log_line)
        self.basic_sched_layout.addWidget(self.help_text)
        self.basic_sched_layout.addStretch(1)
        self.basic_sched_layout.addWidget(self.confirm_button)
        self.basic_sched_edit.setLayout(self.basic_sched_layout)
        self.basic_sched_edit.show()

    def weekdays(self):

        logging.debug('weekdays() called')

        self.weekday_input = QWidget()
        self.weekday_layout = QVBoxLayout(self.weekday_input)

        self.weekday_txt = QLabel()
        self.weekday_txt.setText(QC.translate('', 'Day of week:'))

        self.weekday_layout.addWidget(self.weekday_txt)

        self.weekday_input.hide()

        self.options_box_layout.addWidget(self.weekday_input)

    def interval(self):

        logging.debug('interval() called')

        self.interval_input = QWidget()
        self.interval_layout = QVBoxLayout(self.interval_input)

        self.interval_txt = QLabel()
        self.interval_txt.setText(QC.translate('', 'Every'))

        self.interval_layout.addWidget(self.interval_txt)

        self.interval_input.hide()

        self.options_box_layout.addWidget(self.interval_input)

    def int_time(self):

        logging.debug('int_time() called')

        self.int_time_input = QWidget()
        self.int_time_layout = QVBoxLayout(self.int_time_input)

        self.int_time_txt = QLabel()
        self.int_time_txt.setText(QC.translate('', 'Interval between times'))

        self.int_time_layout.addWidget(self.int_time_txt)

        self.int_time_input.hide()

        self.options_box_layout.addWidget(self.int_time_input)


    def indexChanged(self, event):

        current_index = event
        logging.debug('indexChanged() called {}'.format(current_index))

        if current_index     == 0:
            self.weekday_input.show()
            self.interval_input.hide()
            self.int_time_input.hide()
        elif current_index   == 1:
            self.interval_input.show()
            self.weekday_input.hide()
            self.int_time_input.hide()
        elif current_index  == 2:
            self.int_time_input.show()
            self.weekday_input.hide()
            self.interval_input.hide()


    def edit_done(self):

        logging.debug('edit_done() called BinanceSched')
        
        mode_index  = self.selectMode.currentIndex()
        log_state       = self.log_checkbox.isChecked()
        try:
            offset = int(self.offset_input.text())
        except Exception as e:
            offset = 0

        # interval-str, inteval-index, offset, log-state
        self.config = (mode_index, offset, log_state)

        self.addFunction(BasicScheduler)


class BasicScheduler(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        logging.debug('__init__() called BasicScheduler')

    def execute(self, record):

        interval_str, interval_index, offset, log_state = self.config

        if isinstance(record, tuple) and isinstance(record[0], datetime.datetime):
            
            while record[0] > datetime.datetime.now():
                sleep(1)

            record = record[1]
            target = (self.row + 1, self.column)
            log_txt = '{BASIC SCHEDULER}      '
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
