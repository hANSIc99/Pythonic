from PyQt5.QtCore import pyqtSignal, QVariant
from PyQt5.QtGui import  QIntValidator
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QWidget, QComboBox,
        QCheckBox, QFileDialog, QPushButton, QLineEdit)
from PyQt5.QtCore import QCoreApplication as QC
import logging, os
from Pythonic.elementmaster import ElementMaster
from Pythonic.elementeditor import ElementEditor
from Pythonic.elements.basic_stack_window import StackWindow
from Pythonic.elements.basic_stack_func import StackFunction

class ExecStack(ElementMaster):

    pixmap_path = 'images/ExecStack.png'
    child_pos = (True, False)

    update_stack = pyqtSignal(str, name='update_stack')

    def __init__(self, row, column):
        self.row = row
        self.column = column

        self.show_window = False

        # filename, rel_path, read_mode, write_mode, b_array_limits, n_array_limits, log_state
        filename = None
        rel_path = False
        read_mode = 0
        write_mode = 0
        delete_read = False
        b_array_limits = False
        n_array_limits = None
        log_state = False
        self.config = (filename, rel_path, read_mode, write_mode, delete_read,
                b_array_limits, n_array_limits, log_state)
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('ExecStack called at row {}, column {}'.format(row, column))

        self.addFunction(StackFunction)

    def __setstate__(self, state):
        logging.debug('__setstate__() called ExecStack')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(StackFunction)

    def __getstate__(self):
        logging.debug('__getstate__() called ExecStack')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('openEditor() called ExecStack')

    def toggle_debug(self):
        logging.debug('ExecStack::toggle_debug() called OVERWRITTEN method')
        self.stackWindow = StackWindow(self)
        # diable debug button
        self.icon_bar.debug_button.debug_pressed.disconnect()
        self.icon_bar.debug_button.disableMouseEvent()
        # enable debug button when window is closed
        self.stackWindow.closed.connect(self.reconnect_debug_button)
        self.stackWindow.closed.connect(self.icon_bar.debug_button.enableMouseEvent)
        # connect the update signal
        self.update_stack.connect(self.stackWindow.updateStack)

        # pass filename to the window
        filename = self.config[0]
        rel_path = self.config[1]

        if rel_path and filename:
            filepath = os.path.join(os.environ['HOME'], filename)
        else:
            filepath = filename

        self.stackWindow.raiseWindow(filepath)

    def reconnect_debug_button(self):

        self.icon_bar.debug_button.debug_pressed.connect(
                self.icon_bar.click_debug_element)


    def highlightStop(self):

        logging.debug('ExecStack::highlightStop() called OVERWRITTEN method')
        # pass filename
        filename = self.config[0]
        rel_path = self.config[1]

        if rel_path and filename:
            filepath = os.path.join(os.environ['HOME'], filename)
        else:
            filepath = filename

        self.update_stack.emit(filepath)
        super().highlightStop()

    def edit(self):
        logging.debug('edit() called ExecStack')

        # filename, rel_path, read_mode, write_mode, array_limits, log_state
        self.filename, self.rel_path, self.read_mode, self.write_mode, self.delete_read, \
                self.b_array_limits, self.n_array_limits, log_state = self.config

        self.returnEditLayout = QVBoxLayout()

        self.returnEdit = ElementEditor(self)
        self.returnEdit.setWindowTitle(QC.translate('', 'Stack'))

        self.top_text = QLabel()
        self.top_text.setText(QC.translate('', 'Choose file on hard disc for storing stack data:'))

        self.filename_text = QLabel()
        self.filename_text.setWordWrap(True)

        self.file_button = QPushButton(QC.translate('', 'Select model output file'))
        self.file_button.clicked.connect(self.ChooseFileDialog)
        
        self.relative_file_check = QWidget()
        self.relative_file_check_layout = QHBoxLayout(self.relative_file_check)

        self.relative_file_label = QLabel()
        self.relative_file_label.setText(QC.translate('', 'Filename relative to $HOME.'))
        self.relative_file_checkbox = QCheckBox()
        self.relative_file_check_layout.addWidget(self.relative_file_checkbox)
        self.relative_file_check_layout.addWidget(self.relative_file_label)
        self.relative_file_check_layout.addStretch(1)

        self.relative_filepath_input = QLineEdit()
        self.relative_filepath_input.setPlaceholderText('my_folder/my_file')

        self.file_input = QWidget()
        self.file_input_layout = QVBoxLayout(self.file_input)
        self.file_input_layout.addWidget(self.filename_text)
        self.file_input_layout.addWidget(self.file_button)
        self.file_input_layout.addWidget(self.relative_file_check)
        self.file_input_layout.addWidget(self.relative_filepath_input)


        self.writeInput()
        self.readOutput()
        self.loadLastConfig()


        self.mode_text = QLabel()
        self.mode_text.setText(QC.translate('', 'Configuration:'))

        self.help_text = QWidget()
        self.help_text_layout = QVBoxLayout(self.help_text)

        #self.help_text_1 = QLabel()
        # List
        #self.help_text_1.setText(QC.translate('', 'On input: Write / Read')) 


        # Input: Liste
        #self.help_text_2 = QLabel()
        #self.help_text_2.setText(QC.translate('', 'Insert /Append'))

        # Option: Remove output
        # Output: Liste: First Out /  Last Out / all Out 
        #self.help_text_3 = QLabel()
        #self.help_text_3.setText(QC.translate('', 'Help Text 3'))

        #self.help_text_layout.addWidget(self.help_text_1)
        #self.help_text_layout.addWidget(self.help_text_2)
        #self.help_text_layout.addWidget(self.help_text_3)


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


        self.log_checkbox.setChecked(log_state)

        #signals and slots
        self.confirm_button.clicked.connect(self.returnEdit.closeEvent)
        self.returnEdit.window_closed.connect(self.edit_done)
        self.relative_file_checkbox.stateChanged.connect(self.toggleFileInput)
        self.returnEditLayout.addWidget(self.top_text)
        self.returnEditLayout.addWidget(self.file_input)
        self.returnEditLayout.addWidget(self.mode_text)
        self.returnEditLayout.addWidget(self.write_input)
        self.returnEditLayout.addWidget(self.read_input)
        self.returnEditLayout.addWidget(self.delete_read_widget)
        #self.returnEditLayout.addWidget(self.help_text)
        self.returnEditLayout.addStretch(1)
        self.returnEditLayout.addWidget(self.log_line)
        self.returnEditLayout.addWidget(self.confirm_button)
        self.returnEdit.setLayout(self.returnEditLayout)
        self.returnEdit.show()

    def loadLastConfig(self):

        self.select_read_mode.setCurrentIndex(self.read_mode)
        self.select_write_mode.setCurrentIndex(self.write_mode)
        self.relative_file_checkbox.setChecked(self.rel_path)

        if self.b_array_limits:
            self.enableArrLimits()
            self.array_limits_cbox.setChecked(True)
            if self.n_array_limits:
                self.max_array_elements.setText(str(self.n_array_limits))

        else:
            self.diableArrLimits()
            self.array_limits_cbox.setChecked(False)

        if self.delete_read:
            self.delete_read_checkbox.setChecked(True)
        else:
            self.delete_read_checkbox.setChecked(False)
        
        if self.rel_path:
            self.toggleFileInput(2)
            if self.filename:
                self.relative_filepath_input.setText(self.filename)
        else:
            self.toggleFileInput(0)
            if self.filename:
                self.filename_text.setText(self.filename)

    def toggleFileInput(self, event):
        logging.debug('ExecStack::toggleFileInput() called: {}'.format(event))
        # 0 = FALSE, 2 = TRUE
        if event: # TRUE
            self.file_button.setDisabled(True)
            self.relative_filepath_input.setDisabled(False)
            self.filename_text.setText('')
        else:
            self.file_button.setDisabled(False)
            self.relative_filepath_input.clear()
            self.relative_filepath_input.setDisabled(True)
            self.relative_filepath_input.setPlaceholderText('my_folder/my_file')

    def ChooseFileDialog(self, event):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, \
                QC.translate('', 'Choose file'),"","All Files (*);;Text Files (*.txt)", \
                options=options)
        if fileName:
            logging.debug('ExecStack::ChooseFileDialog() called with filename: {}'.format(fileName))
            self.filename = fileName
            self.filename_text.setText(self.filename)

    def writeInput(self):

        self.write_input = QWidget()
        self.write_layout = QVBoxLayout(self.write_input)

        self.write_input_line = QWidget()
        self.write_input_layout = QHBoxLayout(self.write_input_line)

        self.array_config = QWidget()
        self.array_config_layout = QHBoxLayout(self.array_config)

        self.outpub_behaviour = QWidget()
        self.output_behaviour_layout = QHBoxLayout()

        self.write_txt = QLabel()
        self.write_txt.setText(QC.translate('', 'Do this with input:'))

        self.select_write_mode = QComboBox()
        self.select_write_mode.addItem(QC.translate('', 'Nothing'), QVariant('none'))
        self.select_write_mode.addItem(QC.translate('', 'Insert'), QVariant('i'))
        self.select_write_mode.addItem(QC.translate('', 'Append'), QVariant('a'))

        # maximum array size
        self.array_limits_cbox = QCheckBox()
        self.array_limits_cbox.stateChanged.connect(self.toggleArrayLimits)

        

        self.array_limit_txt = QLabel()
        self.array_limit_txt.setText(QC.translate('', 'Max. array elements:'))

        self.max_array_elements = QLineEdit()
        self.max_array_elements.setValidator(QIntValidator(1, 999))
        self.max_array_elements.setPlaceholderText(QC.translate('', 'Default value: 20'))


        self.array_config_layout.addWidget(self.array_limits_cbox)
        self.array_config_layout.addWidget(self.array_limit_txt)
        self.array_config_layout.addWidget(self.max_array_elements)



        self.write_input_layout.addWidget(self.write_txt)
        self.write_input_layout.addWidget(self.select_write_mode)
        #self.write_layout.addWidget(self.array_limits)

        self.write_layout.addWidget(self.write_input_line)
        self.write_layout.addWidget(self.array_config)

        #self.variable_box.addWidget(self.write_input)

    def toggleArrayLimits(self, event):

        #einzeln aufrufen beim laden der config

        if self.array_limits_cbox.isChecked():
            self.enableArrLimits()
        else:
            self.diableArrLimits()

    def toggleReadBehaviour(self, event):

        if self.delete_read_checkbox.isChecked():
            self.delete_read_checkbox.setChecked(True)
        else:
            self.delete_read_checkbox.setChecked(False)

            
    def enableArrLimits(self):

        self.max_array_elements.setEnabled(True)
        self.max_array_elements.setPlaceholderText(QC.translate('', 'Default value: 20'))

    def diableArrLimits(self):

        self.max_array_elements.setEnabled(False)
        self.max_array_elements.setPlaceholderText(QC.translate('', 'Unlimited'))


    def readOutput(self):

        self.read_input = QWidget()
        self.read_layout = QHBoxLayout(self.read_input)

        self.delete_read_widget = QWidget()
        self.delete_read_layout = QHBoxLayout(self.delete_read_widget)

        self.read_txt = QLabel()
        self.read_txt.setText(QC.translate('', 'Do this when triggered:'))

        self.select_read_mode = QComboBox()
        self.select_read_mode.addItem(QC.translate('', 'Nothing'), QVariant('none'))
        self.select_read_mode.addItem(QC.translate('', 'Pass through'), QVariant('pass'))
        self.select_read_mode.addItem(QC.translate('', 'First out'), QVariant('fo'))
        self.select_read_mode.addItem(QC.translate('', 'Last out'), QVariant('lo'))
        self.select_read_mode.addItem(QC.translate('', 'All out'), QVariant('all'))


        # the delete_read widget is added in the edit() method
        self.delete_read_txt = QLabel()
        self.delete_read_txt.setText(QC.translate('', 'Delete object after read?'))

        self.delete_read_checkbox = QCheckBox()
        self.delete_read_checkbox.stateChanged.connect(self.toggleReadBehaviour)

        self.delete_read_layout.addWidget(self.delete_read_txt)
        self.delete_read_layout.addWidget(self.delete_read_checkbox)

        self.read_layout.addWidget(self.read_txt)
        self.read_layout.addWidget(self.select_read_mode)


    def edit_done(self):
        logging.debug('edit_done() called ExecStack' )

        if self.max_array_elements.text() == '':
            n_array_limits = None        
        else:
            n_array_limits = int(self.max_array_elements.text())

        log_state = self.log_checkbox.isChecked()
        write_mode = self.select_write_mode.currentIndex()
        read_mode = self.select_read_mode.currentIndex()
        b_array_limits = self.array_limits_cbox.isChecked()
        delete_read = self.delete_read_checkbox.isChecked()
        n_array_limits
        filename = self.filename
        rel_path            = self.relative_file_checkbox.isChecked()
        if rel_path:
            filename        = self.relative_filepath_input.text()
        else:
            filename        = self.filename

        if filename == '':
            filename = None

        # filename, read_mode, write_mode, b_array_limits, n_array_limits, log_state
        self.config = (filename, rel_path, read_mode, write_mode, delete_read, b_array_limits, \
                n_array_limits, log_state)
        self.addFunction(StackFunction)
