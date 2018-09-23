from elementmaster import ElementMaster
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant, QRegExp
from PyQt5.QtGui import  QPixmap, QPainter, QColor, QIntValidator, QRegExpValidator
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
        self.selectMode.addItem(QC.translate('', 'Interval between times'), QVariant('time_between'))
        self.selectMode.addItem(QC.translate('', 'At specific time'), QVariant('time'))

        self.options_box = QWidget()
        self.options_box_layout = QVBoxLayout(self.options_box)
        self.interval()
        self.at_time()
        self.time_between()
        self.on_weekdays()


        self.help_text_1 = QLabel()
        self.help_text_1.setText(QC.translate('', 'Start subsequent actions after your requirements.')) 

        self.log_line = QWidget()
        self.ask_for_logging = QLabel()
        self.ask_for_logging.setText(QC.translate('', 'Log output?'))
        self.log_checkbox = QCheckBox()
        self.log_line_layout = QHBoxLayout(self.log_line)
        self.log_line_layout.addWidget(self.ask_for_logging)
        self.log_line_layout.addWidget(self.log_checkbox)
        self.log_line_layout.addStretch(1)

        # load config

        #self.selectMode.setCurrentIndex(mode_index)
        self.selectMode.setCurrentIndex(1) #anpassen

        self.loadLastConfig()

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
        
        self.basic_sched_layout.addWidget(self.log_line)
        self.basic_sched_layout.addWidget(self.help_text_1)
        self.basic_sched_layout.addStretch(1)
        self.basic_sched_layout.addWidget(self.confirm_button)
        self.basic_sched_edit.setLayout(self.basic_sched_layout)
        self.basic_sched_edit.show()


    def at_time(self):

        logging.debug('at_time() called')

        self.at_time_input = QWidget()
        self.at_time_layout = QVBoxLayout(self.at_time_input)

        self.time_text = QLabel()
        self.time_text.setText(QC.translate('', 'At:'))

        self.time_input = QLineEdit()
        regexp_validator = QRegExp('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$')
        self.time_validator = QRegExpValidator(regexp_validator)
        self.time_input.setValidator(self.time_validator)
        self.time_input.setPlaceholderText(QC.translate('', 'hh:mm'))

        self.at_time_layout.addWidget(self.time_text)
        self.at_time_layout.addWidget(self.time_input)

        self.at_time_input.hide()
        self.at_time_layout.addWidget(self.at_time_input)

        self.at_time_input.hide()
        self.options_box_layout.addWidget(self.at_time_input)

    def on_weekdays(self):

        logging.debug('on_weekdays() called')

        self.on_weekdays_input = QWidget()
        self.on_weekdays_layout = QVBoxLayout(self.on_weekdays_input)
        

        self.weekday_txt = QLabel()
        self.weekday_txt.setText(QC.translate('', 'On:'))

        self.check_monday       = QCheckBox()
        self.check_tuesday      = QCheckBox()
        self.check_wednesday    = QCheckBox()
        self.check_thursday     = QCheckBox()
        self.check_friday       = QCheckBox()
        self.check_saturday     = QCheckBox()
        self.check_sunday       = QCheckBox()

        self.txt_monday         = QLabel()
        self.txt_tuesday        = QLabel()
        self.txt_wednesday      = QLabel()
        self.txt_thursday       = QLabel()
        self.txt_friday         = QLabel()
        self.txt_saturday       = QLabel()
        self.txt_sunday         = QLabel()

        self.txt_monday.setText(QC.translate('', 'Monday'))
        self.txt_tuesday.setText(QC.translate('', 'Tuesday'))
        self.txt_wednesday.setText(QC.translate('', 'Wednesday'))
        self.txt_thursday.setText(QC.translate('', 'Thursday'))
        self.txt_friday.setText(QC.translate('', 'Friday'))
        self.txt_saturday.setText(QC.translate('', 'Saturday'))
        self.txt_sunday.setText(QC.translate('', 'Sunday'))

        self.mon_tue_wed = QWidget()
        self.mon_tue_wed_layout = QHBoxLayout(self.mon_tue_wed)
        self.mon_tue_wed_layout.addWidget(self.txt_monday)
        self.mon_tue_wed_layout.addWidget(self.check_monday)
        self.mon_tue_wed_layout.addWidget(self.txt_tuesday)
        self.mon_tue_wed_layout.addWidget(self.check_tuesday)
        self.mon_tue_wed_layout.addWidget(self.txt_wednesday)
        self.mon_tue_wed_layout.addWidget(self.check_wednesday)
        self.mon_tue_wed_layout.addStretch(1)

        self.thu_fri_sat = QWidget()
        self.thu_fri_sat_layout = QHBoxLayout(self.thu_fri_sat)
        self.thu_fri_sat_layout.addWidget(self.txt_thursday)
        self.thu_fri_sat_layout.addWidget(self.check_thursday)
        self.thu_fri_sat_layout.addWidget(self.txt_friday)
        self.thu_fri_sat_layout.addWidget(self.check_friday)
        self.thu_fri_sat_layout.addWidget(self.txt_saturday)
        self.thu_fri_sat_layout.addWidget(self.check_saturday)
        self.thu_fri_sat_layout.addStretch(1)

        self.sun = QWidget()
        self.sun_layout = QHBoxLayout(self.sun)
        self.sun_layout.addWidget(self.txt_sunday)
        self.sun_layout.addWidget(self.check_sunday)
        self.sun_layout.addStretch(1)

        
        self.on_weekdays_layout.addWidget(self.weekday_txt)
        self.on_weekdays_layout.addWidget(self.mon_tue_wed)
        self.on_weekdays_layout.addWidget(self.thu_fri_sat)
        self.on_weekdays_layout.addWidget(self.sun)

        self.on_weekdays_input.hide()

        self.options_box_layout.addWidget(self.on_weekdays_input)

    def interval(self):

        logging.debug('interval() called')

        self.interval_input = QWidget()
        self.interval_layout = QVBoxLayout(self.interval_input)

        self.time_base_input_line = QWidget()
        self.time_base_input_layout = QHBoxLayout(self.time_base_input_line)

        self.interval_txt = QLabel()
        self.interval_txt.setText(QC.translate('', 'Every'))

        self.repeat_val_input = QLineEdit()
        self.repeat_val_input.setValidator(QIntValidator(1, 9999))
        self.repeat_val_input.setText('1')

        self.time_base_input = QComboBox()
        self.time_base_input.addItem(QC.translate('', 'Seconds'), QVariant('sec'))
        self.time_base_input.addItem(QC.translate('', 'Minutes'), QVariant('min'))
        self.time_base_input.addItem(QC.translate('', 'Hours'), QVariant('hour'))

        self.time_base_input_layout.addWidget(self.repeat_val_input)
        self.time_base_input_layout.addWidget(self.time_base_input)

        self.interval_layout.addWidget(self.interval_txt)
        self.interval_layout.addWidget(self.time_base_input_line)

        self.interval_input.hide()

        self.options_box_layout.addWidget(self.interval_input)

    def time_between(self):

        logging.debug('time_between() called')

        self.time_between_input = QWidget()
        self.time_between_layout = QVBoxLayout(self.time_between_input)

        self.time_between_txt = QLabel()
        self.time_between_txt.setText(QC.translate('', 'Between'))

        regexp_validator = QRegExp('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$')
        self.time_validator = QRegExpValidator(regexp_validator)

        self.time_row = QWidget()
        self.time_row_layout = QHBoxLayout(self.time_row)

        self.start_time_input = QLineEdit()
        self.start_time_input.setValidator(self.time_validator)
        self.start_time_input.setPlaceholderText(QC.translate('', 'hh:mm (default 00:00)'))

        self.and_text = QLabel()
        self.and_text.setText(QC.translate('', 'and'))

        self.stop_time_input = QLineEdit()
        self.stop_time_input.setValidator(self.time_validator)
        self.stop_time_input.setPlaceholderText(QC.translate('', 'hh:mm (default 00:00)'))

        
        self.time_row_layout.addWidget(self.start_time_input)
        self.time_row_layout.addWidget(self.and_text)
        self.time_row_layout.addWidget(self.stop_time_input)


        self.time_between_layout.addWidget(self.time_between_txt)
        self.time_between_layout.addWidget(self.time_row)

        self.time_between_input.hide()

        self.options_box_layout.addWidget(self.time_between_input)


    def indexChanged(self, event):

        current_index = event
        logging.debug('indexChanged() called {}'.format(current_index))

        if current_index     == 0:  # Interval
            self.interval_input.show()
            self.at_time_input.hide()
            self.time_between_input.hide()
            self.on_weekdays_input.hide()
        elif current_index   == 1:  # Interval between times
            self.interval_input.show()
            self.time_between_input.show()
            self.on_weekdays_input.show()
            self.at_time_input.hide()
        elif current_index  == 2:   # At specific time
            self.time_between_input.hide()
            self.at_time_input.show()
            self.on_weekdays_input.show()
            self.interval_input.hide()

    def loadLastConfig(self):

        #ta_str, ta_index, ta_config, log_state = self.config

        #logging.debug('loadLastConfig() called with ta_str = {}'.format(ta_str))

        self.indexChanged(1)

    def parse_time(self, time_input):

            if not time_input == '' :
                try:
                    hour, minute = time_input.split(':')  
                    hour = int(hour)
                    minute = int(minute)
                except Exception as e:
                    hour = int(time_input)
                    minute = 0
            else:
                hour = 0
                minute = 0

            return (hour, minute)

    def get_days(self):

        logging.debug('get_days() called')

        check_monday    = self.check_monday.isChecked()
        check_tuesday   = self.check_tuesday.isChecked()
        check_wednesday = self.check_wednesday.isChecked()
        check_thursday  = self.check_thursday.isChecked()
        check_friday    = self.check_friday.isChecked()
        check_saturday  = self.check_saturday.isChecked()
        check_sunday    = self.check_sunday.isChecked()

        logging.debug('Mon {}, Tue {}, Wed {}, Thu {}, Fri {}, Sat {}, Sun {}'.format(
            check_monday, check_tuesday, check_wednesday, check_thursday, check_friday,
            check_saturday, check_sunday) )

        return (check_monday, check_tuesday, check_wednesday,
                   check_thursday, check_friday, check_saturday,
                   check_sunday)



    def edit_done(self):

        logging.debug('edit_done() called BinanceSched')
        
        mode_index  = self.selectMode.currentIndex()
        log_state       = self.log_checkbox.isChecked()
        # mode-index, mode-data, log_state

        if mode_index       == 0: #Interval

            logging.debug('mode_index = 0')
            repeat_val = self.repeat_val_input.text()
            time_base = self.time_base_input.currentIndex()
            # 0 = Seconds
            # 1 = Minutes
            # 2 = Hours

            mode_data = (repeat_val, time_base)

        elif mode_index     == 1: # Interval between times

            logging.debug('mode_index = 1')

            repeat_val = self.repeat_val_input.text()
            time_base = self.time_base_input.currentIndex()
            # 0 = Seconds
            # 1 = Minutes
            # 2 = Hours
            start_time_input = self.start_time_input.text()
            start_time = self.parse_time(start_time_input)

            logging.debug('Start hour {} - Start minute {}'.format(start_time[0], start_time[1]))

            stop_time_input = self.stop_time_input.text()
            stop_time = self.parse_time(stop_time_input)

            logging.debug('Stop hour {} - Stop minute {}'.format(stop_time[0], stop_time[1]))

            active_days = self.get_days()

            mode_data = (repeat_val, time_base, start_time, stop_time, active_days)

        elif mode_index     == 2: # At specific time
            logging.debug('mode_index = 2')

        mode_data = None


        self.config = (mode_index, mode_data, log_state)

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
