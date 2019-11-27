from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget,
                            QComboBox, QCheckBox, QFileDialog, QLineEdit)
from PyQt5.QtCore import QCoreApplication as QC
import logging
from Pythonic.elementeditor import ElementEditor
from Pythonic.elementmaster import ElementMaster
from Pythonic.elements.ml_svm_predict_func import MLSVM_PredictFunction
from pathlib import Path

class MLSVM_Predict(ElementMaster):

    pixmap_path = 'images/MLSVM_Predict.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        # scale_option, scale_mean, scale_std, predict_val, filename, log_state
        
        scale_option        = 0
        scale_mean          = True
        scale_std           = True
        predict_val         = False
        filename            = None
        rel_path            = False
        log_state           = False

        self.config = scale_option, scale_mean, scale_std, predict_val, filename, rel_path, log_state

        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('MLSVM_Predict::__init__() called at row {}, column {}'.format(row, column))
        self.addFunction(MLSVM_PredictFunction)

    def __setstate__(self, state):
        logging.debug('MLSVM_Predict::__setstate__() called')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, self.pixmap_path, True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(MLSVM_PredictFunction)

    def __getstate__(self):
        logging.debug('MLSVM_Predict::__getstate__() called')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('MLSVM_Predict::openEditor() called')

    def edit(self):

        logging.debug('MLSVM_Predict::edit()')

        # scale_option, scale_mean, scale_std, predict_val, filename, log_state
        self.scale_option, self.scale_mean, self.scale_std, self.predict_val, \
                self.filename, self.rel_path, self.log_state = self.config

        self.home_dict = str(Path.home())

        self.scale_label = QLabel()
        self.scale_label.setText(QC.translate('', 'Scale n_samples ?'))
        self.scale_list = QComboBox()
        self.scale_list.addItem(QC.translate('', 'No'), QVariant(False))
        self.scale_list.addItem(QC.translate('', 'Yes'), QVariant(True))

        
        self.scale_center_input_line = QWidget()
        self.scale_center_input_line_layout = QHBoxLayout(self.scale_center_input_line)
        self.scale_center_label = QLabel()
        self.scale_center_label.setText(QC.translate('', 'Center data before scaling?'))
        self.scale_center_checkbox = QCheckBox()
        self.scale_center_input_line_layout.addWidget(self.scale_center_label)
        self.scale_center_input_line_layout.addWidget(self.scale_center_checkbox)

        self.scale_std_input_line = QWidget()
        self.scale_std_input_line_layout = QHBoxLayout(self.scale_std_input_line)
        self.scale_std_label = QLabel()
        self.scale_std_label.setText(QC.translate('', 'Scale data until variance?'))
        self.scale_std_checkbox = QCheckBox()
        self.scale_std_input_line_layout.addWidget(self.scale_std_label)
        self.scale_std_input_line_layout.addWidget(self.scale_std_checkbox)

        self.scale_input_area = QWidget()
        self.scale_input_area_layout = QVBoxLayout(self.scale_input_area)
        self.scale_input_area_layout.addWidget(self.scale_center_input_line)
        self.scale_input_area_layout.addWidget(self.scale_std_input_line)

        self.last_value_line = QWidget()
        self.last_value_line_layout = QHBoxLayout(self.last_value_line)
        self.last_value_label = QLabel()
        self.last_value_label.setText(
                QC.translate('', 'Predict only last value [-1]?'))
        self.last_value_checkbox = QCheckBox()

        self.last_value_line_layout.addWidget(self.last_value_label)
        self.last_value_line_layout.addWidget(self.last_value_checkbox)


        self.conn_rest_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        """
        self.filename_text = QLabel()
        self.filename_text.setWordWrap(True)
        
        self.file_button = QPushButton(QC.translate('', 'Select model file'))
        self.file_button.clicked.connect(self.openFileNameDialog)
        """

        self.filename_text = QLabel()
        self.filename_text.setWordWrap(True)

        self.file_button = QPushButton(QC.translate('', 'Select model output file'))
        self.file_button.clicked.connect(self.openFileNameDialog)
        
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

        """
        output: prediction quality
        """
        self.help_text_1 = QLabel()
        self.help_text_1.setText(QC.translate('', 'Expects an array of samples as input.'))

        self.help_text_2 = QLabel()
        self.help_text_2.setText(QC.translate('', 'Outputs a single value or an array.'))

        

        # hier logging option einfügen
        self.log_line = QWidget()
        self.ask_for_logging = QLabel()
        self.ask_for_logging.setText(QC.translate('', 'Log output?'))
        self.log_checkbox = QCheckBox()
        self.log_line_layout = QHBoxLayout(self.log_line)
        self.log_line_layout.addWidget(self.ask_for_logging)
        self.log_line_layout.addWidget(self.log_checkbox)
        self.log_line_layout.addStretch(1)

        
        self.ml_svm_predict_edit = ElementEditor(self)
        self.ml_svm_predict_edit.setWindowTitle(QC.translate('', 'Support Vector Machine Prediction'))
        self.ml_svm_predict_edit.setMinimumHeight(450)

        # signals and slots
        self.relative_file_checkbox.stateChanged.connect(self.toggleFileInput)
        self.scale_list.currentIndexChanged.connect(self.scaledIndexChanged)
        self.confirm_button.clicked.connect(self.ml_svm_predict_edit.closeEvent)
        self.ml_svm_predict_edit.window_closed.connect(self.edit_done)

        # load config
        self.loadLastConfig()

        self.conn_rest_layout.addWidget(self.help_text_1)
        self.conn_rest_layout.addWidget(self.scale_label) # scale: copy = false
        self.conn_rest_layout.addWidget(self.scale_list)
        self.conn_rest_layout.addWidget(self.scale_input_area)
        self.conn_rest_layout.addWidget(self.last_value_line)
        self.conn_rest_layout.addWidget(self.file_input)
        self.conn_rest_layout.addStretch(1)
        self.conn_rest_layout.addWidget(self.help_text_2)
        self.conn_rest_layout.addWidget(self.log_line)
        self.conn_rest_layout.addWidget(self.confirm_button)
        self.ml_svm_predict_edit.setLayout(self.conn_rest_layout)
        self.ml_svm_predict_edit.show()

    def loadLastConfig(self):

        logging.debug('MLSVM_Predict::loadLastConfig() called')
        
        self.scale_list.setCurrentIndex(self.scale_option)
        self.scaledIndexChanged(self.scale_option)
        self.scale_center_checkbox.setChecked(self.scale_mean)
        self.scale_std_checkbox.setChecked(self.scale_std)
        self.last_value_checkbox.setChecked(self.predict_val)
        self.log_checkbox.setChecked(self.log_state)
        self.relative_file_checkbox.setChecked(self.rel_path)
        
        if self.rel_path:
            self.toggleFileInput(2)
            if self.filename:
                self.relative_filepath_input.setText(self.filename)
        else:
            self.toggleFileInput(0)
            if self.filename:
                self.filename_text.setText(self.filename)

    def toggleFileInput(self, event):
        logging.debug('MLSVM::toggleFileInput() called: {}'.format(event))
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

    def scaledIndexChanged(self, event):

        current_index = event
        logging.debug('MLSVM_Predict::scaledIndexChanged() called: {}'.format(event))
        if event == 1 :
            self.scale_input_area.setVisible(True)
        else:
            self.scale_input_area.setVisible(False)

    def openFileNameDialog(self, event):    
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getOpenFileName(self, QC.translate('', 'Open SVM model file'),
                self.home_dict,"All Files (*);;Pythonic Files (*.pyc)", options=options)
        if fileName:
            logging.debug('MLSVM_Predict::openFileNameDialog() called with filename: {}'.format(fileName))
            self.filename = fileName
            self.filename_text.setText(self.filename)


    def edit_done(self):

        logging.debug('MLSVM_Predict::edit_done() called')
        # scale_option, scale_mean, scale_std, predict_val, filename, log_state

        scale_option        = self.scale_list.currentIndex()
        scale_mean          = self.scale_center_checkbox.isChecked()
        scale_std           = self.scale_std_checkbox.isChecked()
        predict_val         = self.last_value_checkbox.isChecked()
        log_state           = self.log_checkbox.isChecked()
        rel_path            = self.relative_file_checkbox.isChecked()
        if rel_path:
            filename        = self.relative_filepath_input.text()
        else:
            filename        = self.filename

        if filename == '':
            filename = None

        self.config = scale_option, scale_mean, scale_std, predict_val, filename, rel_path, log_state
        
        self.addFunction(MLSVM_PredictFunction)
