from PyQt5.QtCore import Qt, pyqtSignal, QVariant
from PyQt5.QtGui import  QIntValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QComboBox, QCheckBox, QStackedWidget
from PyQt5.QtCore import QCoreApplication as QC
import logging
from Pythonic.elementmaster import ElementMaster
from Pythonic.elementeditor import ElementEditor
from Pythonic.elements.basic_ta_func import TAFunction

class ExecTA(ElementMaster):

    pixmap_path = 'images/ExecTA.png'
    child_pos = (True, False)

    def __init__(self, row, column):

        self.row = row
        self.column = column

        ta_str = 'MA'
        ta_index = 0
        ta_config = (3, )
        log_state = False

        self.config = (ta_str, ta_index, ta_config, log_state)

        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('ExecTA called at row {}, column {}'.format(row, column))
        self.addFunction(TAFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecTA')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(TAFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecTA')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called ExecTA')

    def edit(self):

        logging.debug('edit() called ExecTA')

        ta_str, ta_index, ta_config, log_state = self.config

        self.basic_ta_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.interval_txt = QLabel()
        self.interval_txt.setText(QC.translate('', 'Choose technical analysis function'))

        # https://github.com/sammchardy/python-binance/blob/master/binance/client.py
        self.selectTA = QComboBox()
        self.selectTA.addItem(QC.translate('', 'Moving Average'), QVariant('MA'))
        self.selectTA.addItem(QC.translate('', 'Exponential Moving Average'), QVariant('EMA'))
        self.selectTA.addItem(QC.translate('', 'Stochastic Oscillator %K'), QVariant('STOK'))
        self.selectTA.addItem(QC.translate('', 'Stochastic Oscillator %D'), QVariant('STO'))
        self.selectTA.addItem(QC.translate('', 'Relative Strenght Index'), QVariant('RSI'))
        """
        self.selectTA.addItem(QC.translate('', 'Momentum'), QVariant('MOM'))
        self.selectTA.addItem(QC.translate('', 'Rate of Change'), QVariant('ROC'))
        self.selectTA.addItem(QC.translate('', 'Average True Range'), QVariant('ATR'))
        self.selectTA.addItem(QC.translate('', 'Bollinger Bands'), QVariant('BBANDS'))
        self.selectTA.addItem(QC.translate('', 'Pivot Points, Support and Resitances'), QVariant('PPSR'))
        self.selectTA.addItem(QC.translate('', 'Trix'), QVariant('TRIX'))
        self.selectTA.addItem(QC.translate('', 'Average Directional Movement Index'), QVariant('ADX'))
        self.selectTA.addItem(QC.translate('', 'MACD, MACD Signal and MACD diffrence'), QVariant('MACD'))
        self.selectTA.addItem(QC.translate('', 'Mass Index'), QVariant('MI'))
        self.selectTA.addItem(QC.translate('', 'Vortex Indikator'), QVariant('VORTEX'))
        self.selectTA.addItem(QC.translate('', 'KST Oscillator'), QVariant('KST'))
        self.selectTA.addItem(QC.translate('', 'True Strenght Index'), QVariant('TSI'))
        self.selectTA.addItem(QC.translate('', 'Accumulation/Distribution'), QVariant('ACCDIST'))
        self.selectTA.addItem(QC.translate('', 'Chaikin Oscillator'), QVariant('CHAI'))
        self.selectTA.addItem(QC.translate('', 'Money Flow Index and Ratio'), QVariant('MFI'))
        self.selectTA.addItem(QC.translate('', 'On Balance Volume'), QVariant('OBV'))
        self.selectTA.addItem(QC.translate('', 'Force Index'), QVariant('FI'))
        self.selectTA.addItem(QC.translate('', 'Ease of Movement'), QVariant('EOM'))
        self.selectTA.addItem(QC.translate('', 'Commodity Channel Index'), QVariant('CCI'))
        """
        self.selectTA.setCurrentIndex(ta_index)


        self.variable_box = QStackedWidget()
        self.maInput()
        self.emaInput()
        self.stokInput()
        self.stoInput()
        self.rsiInput()
        self.loadLastConfig()

        logging.debug('edit() - {} elements in QStackedWidget'.format(self.variable_box.count()))

        self.link_line = QWidget()
        self.link_line_layout = QHBoxLayout(self.link_line)

        self.link_txt = QLabel()
        self.link_txt.setText(QC.translate('', 'Find information about technical analysis on'))

        self.link = QLabel()
        self.link.setText('<a href="https://www.investopedia.com/walkthrough/forex/">Investopedia</a>')
        self.link.setTextFormat(Qt.RichText)
        self.link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.link.setOpenExternalLinks(True)

        self.link_line_layout.addWidget(self.link_txt)
        self.link_line_layout.addWidget(self.link)
        self.link_line_layout.addStretch(1)

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


        self.basic_ta_edit = ElementEditor(self)
        self.basic_ta_edit.setWindowTitle(QC.translate('', 'Edit TA function'))

        # signals and slots
        self.confirm_button.clicked.connect(self.basic_ta_edit.closeEvent)
        self.basic_ta_edit.window_closed.connect(self.edit_done)
        self.selectTA.currentIndexChanged.connect(self.indexChanged)

        self.basic_ta_layout.addWidget(self.interval_txt)
        self.basic_ta_layout.addWidget(self.selectTA)
        self.basic_ta_layout.addWidget(self.variable_box)
        self.basic_ta_layout.addStretch(1)
        self.basic_ta_layout.addWidget(self.log_line)
        self.basic_ta_layout.addWidget(self.link_line)
        self.basic_ta_layout.addWidget(self.confirm_button)
        self.basic_ta_edit.setLayout(self.basic_ta_layout)
        self.basic_ta_edit.show()
        
    def loadLastConfig(self):

        ta_str, ta_index, ta_config, log_state = self.config

        logging.debug('loadLastConfig() called with ta_str = {}'.format(ta_str))

        self.variable_box.setCurrentIndex(ta_index)

        if ta_str == 'MA':
            self.ma_range_input.setText(str(ta_config[0]))
        elif ta_str == 'EMA':
            self.ema_range_input.setText(str(ta_config[0]))
        elif ta_str == 'STO':
            self.sto_range_input.setText(str(ta_config[0]))
        elif ta_str == 'RSI':
            self.rsi_range_input.setText(str(ta_config[0]))

    def maInput(self):

        self.ma_input = QWidget()
        self.ma_layout = QHBoxLayout(self.ma_input)

        self.ma_range_txt = QLabel()
        self.ma_range_txt.setText(QC.translate('', 'Enter time range MA'))

        self.ma_range_input = QLineEdit()
        self.ma_range_input.setValidator(QIntValidator(1, 999))
        self.ma_range_input.setPlaceholderText(QC.translate('', 'Default value: 3'))

        self.ma_layout.addWidget(self.ma_range_txt)
        self.ma_layout.addWidget(self.ma_range_input)


        self.variable_box.addWidget(self.ma_input)

    def emaInput(self):

        self.ema_input = QWidget()
        self.ema_layout = QHBoxLayout(self.ema_input)

        self.ema_range_txt = QLabel()
        self.ema_range_txt.setText(QC.translate('', 'Enter time range EMA'))

        self.ema_range_input = QLineEdit()
        self.ema_range_input.setValidator(QIntValidator(1, 999))
        self.ema_range_input.setPlaceholderText(QC.translate('', 'Default value: 3'))

        self.ema_layout.addWidget(self.ema_range_txt)
        self.ema_layout.addWidget(self.ema_range_input)

        self.variable_box.addWidget(self.ema_input)

    def stokInput(self):

        self.stok_input = QWidget()
        self.stok_layout = QHBoxLayout(self.stok_input)

        self.variable_box.addWidget(self.stok_input)

    def stoInput(self):

        self.sto_input = QWidget()
        self.sto_layout = QHBoxLayout(self.sto_input)

        self.sto_range_txt = QLabel()
        self.sto_range_txt.setText(QC.translate('', 'Enter MA period'))

        self.sto_range_input = QLineEdit()
        self.sto_range_input.setValidator(QIntValidator(1, 999))
        self.sto_range_input.setPlaceholderText(QC.translate('', 'Default value: 3'))

        self.sto_layout.addWidget(self.sto_range_txt)
        self.sto_layout.addWidget(self.sto_range_input)

        self.variable_box.addWidget(self.sto_input)

    def rsiInput(self):

        self.rsi_input = QWidget()
        self.rsi_layout = QHBoxLayout(self.rsi_input)

        self.rsi_range_txt = QLabel()
        self.rsi_range_txt.setText(QC.translate('', 'Enter periods'))

        self.rsi_range_input = QLineEdit()
        self.rsi_range_input.setValidator(QIntValidator(1, 999))
        self.rsi_range_input.setPlaceholderText(QC.translate('', 'Default value: 3'))

        self.rsi_layout.addWidget(self.rsi_range_txt)
        self.rsi_layout.addWidget(self.rsi_range_input)

        self.variable_box.addWidget(self.rsi_input)

    def indexChanged(self, event):

        current_index = event
        logging.debug('indexChanged() called {}'.format(current_index))
        self.variable_box.setCurrentIndex(current_index)

        if current_index == 0:

            logging.debug('Moving Average selected - {}'.format(self.selectTA.currentData()))

        elif current_index == 1:

            logging.debug('Exponential Moving Average selected')

    def edit_done(self):

        logging.debug('edit_done() called ExecTA')
        if self.selectTA.currentData() == 'MA':

            period = self.ma_range_input.text()

            if period == '':
                ta_config = (3, )
            else:
                ta_config = (int(period), )

            logging.debug('edit_done() - Moving Average selected - {}'.format(ta_config))

        elif self.selectTA.currentData() == 'EMA':

            period = self.ema_range_input.text()

            if period == '':
                ta_config = (3, )
            else:
                ta_config = (int(period), )

            logging.debug('edit_done() - Exponential Moving Average selected - {}'.format(ta_config))

        elif self.selectTA.currentData() == 'STO':

            period = self.sto_range_input.text()

            if period == '':
                ta_config = (3, )
            else:
                ta_config = (int(period), )

            logging.debug('edit_done() - Stochastic Oscillator %D or EMA or RSI selected - {}'.format(ta_config))

        elif self.selectTA.currentData() == 'RSI':

            period = self.rsi_range_input.text()

            if period == '':
                ta_config = (3, )
            else:
                ta_config = (int(period), )

            logging.debug('edit_done() - Relative Strenght Index selected - {}'.format(ta_config))


        else:
            ta_config = None


        ta_str    = self.selectTA.currentData()
        ta_index  = self.selectTA.currentIndex()
        log_state = self.log_checkbox.isChecked()

        self.config = (ta_str, ta_index, ta_config, log_state)
        self.addFunction(TAFunction)
