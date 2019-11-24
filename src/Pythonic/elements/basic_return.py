from PyQt5.QtCore import pyqtSignal, QVariant
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QWidget, QComboBox, QCheckBox,
                                QPushButton, QStackedWidget)
from PyQt5.QtCore import QCoreApplication as QC
import logging
from Pythonic.elementmaster import ElementMaster
from Pythonic.elementeditor import ElementEditor
from Pythonic.record_function import alphabet
from Pythonic.elements.basic_return_func import ReturnFunction

class ExecReturn(ElementMaster):

    pixmap_path = 'images/ExecReturn.png'
    child_pos = (False, False)

    query_grid_config = pyqtSignal(name='query_grid_config')

    def __init__(self, row, column):
        self.row = row
        self.column = column
        # grid, wrk_selecctor_index, wrk_pos, ischecked
        self.config = (0, 0, (0,0), False)
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('ExecReturn called at row {}, column {}'.format(row, column))

        self.addFunction(ReturnFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecReturn')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(ReturnFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecReturn')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called ExecReturn')


    def edit(self):
        logging.debug('edit() called ExecReturn')
        self.returnEditLayout = QVBoxLayout()

        self.returnEdit = ElementEditor(self)
        self.returnEdit.setWindowTitle(QC.translate('', 'Edit Return'))

        self.grid_text = QLabel()
        self.grid_text.setText(QC.translate('', 'Go to grid:'))

        self.element_text = QLabel()
        self.element_text.setText(QC.translate('', 'Go to element:'))

        self.help_text = QWidget()
        self.help_text_layout = QVBoxLayout(self.help_text)

        self.help_text_1 = QLabel()
        self.help_text_1.setText(QC.translate('', 'Choose an element from the list')) 

        self.help_text_2 = QLabel()
        self.help_text_2.setText(QC.translate('', 'to which you want to return with the'))

        self.help_text_3 = QLabel()
        self.help_text_3.setText(QC.translate('', 'current input'))

        self.help_text_layout.addWidget(self.help_text_1)
        self.help_text_layout.addWidget(self.help_text_2)
        self.help_text_layout.addWidget(self.help_text_3)


        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        # hier logging option einfügen
        self.log_line = QWidget()
        self.ask_for_logging = QLabel()
        self.ask_for_logging.setText(QC.translate('', 'Log output?'))
        self.log_checkbox = QCheckBox()
        self.log_line_layout = QHBoxLayout(self.log_line)
        self.log_line_layout.addWidget(self.ask_for_logging)
        self.log_line_layout.addWidget(self.log_checkbox)
        self.log_line_layout.addStretch(1)


        self.element_selector = QStackedWidget()

        self.grid_selector = QComboBox()

        # emmiting signal
        self.query_grid_config.emit()
        self.grid_selector.currentIndexChanged.connect(self.gridIndexChanged)

        self.loadLastConfig()

        self.confirm_button.clicked.connect(self.returnEdit.closeEvent)
        self.returnEdit.window_closed.connect(self.edit_done)
        self.returnEditLayout.addWidget(self.grid_text)
        self.returnEditLayout.addWidget(self.grid_selector)
        self.returnEditLayout.addWidget(self.element_text)
        self.returnEditLayout.addWidget(self.element_selector)
        self.returnEditLayout.addWidget(self.log_line)
        self.returnEditLayout.addWidget(self.help_text)
        self.returnEditLayout.addStretch(1)
        self.returnEditLayout.addWidget(self.confirm_button)
        self.returnEdit.setLayout(self.returnEditLayout)
        self.returnEdit.show()

    def recvGridConfig(self, config):

        self.wrk_selectors_arr = []
        logging.debug('ExecReturn::recvGridConfig config: {}'.format(config))
        for index, wrk_area in enumerate(config):
            self.grid_selector.addItem('Grid {}'.format(index + 1))
            logging.debug('ExecReturn::recvGridConfig Grid: {}'.format(index + 1))

            self.wrk_selectors_arr.append(QComboBox())
            logging.debug('ExecReturn::recvGridConfig flag: {}'.format(1))
            self.element_selector.addWidget(self.wrk_selectors_arr[index])
            logging.debug('ExecReturn::recvGridConfig flag: {}'.format(1))
            for pos in wrk_area:
                self.wrk_selectors_arr[index].addItem('{} {}'.format(pos[0], alphabet[pos[1]]), QVariant(pos))

    def gridIndexChanged(self, index):

        logging.debug('ExecReturn::gridIndexChanged() called: {}'.format(index))
        self.element_selector.setCurrentIndex(index)


    def loadLastConfig(self):

        grid, wrk_selector_index, wrk_pos, log_state = self.config

        self.grid_selector.setCurrentIndex(grid)
        self.element_selector.setCurrentIndex(grid)
        self.wrk_selectors_arr[grid].setCurrentIndex(wrk_selector_index)
        self.log_checkbox.setChecked(log_state)

    def edit_done(self):
        logging.debug('edit_done() called ExecReturn' )
        grid = self.grid_selector.currentIndex()
        wrk_selector_index = self.wrk_selectors_arr[grid].currentIndex()
        wrk_pos = self.wrk_selectors_arr[grid].currentData()

        self.config = (grid, wrk_selector_index, wrk_pos, self.log_checkbox.isChecked())
        self.addFunction(ReturnFunction)
