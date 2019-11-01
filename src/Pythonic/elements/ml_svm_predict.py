from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, pyqtSlot, QVariant
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox, QStackedWidget, QFileDialog
from PyQt5.QtCore import QCoreApplication as QC
from pythonic_binance.client import Client
import pandas as pd
import os.path, datetime, logging, requests, json, pickle
from time import sleep
from Pythonic.elementeditor import ElementEditor
from Pythonic.record_function import Record, Function
from Pythonic.elementmaster import ElementMaster
from pathlib import Path
from sys import getsizeof
from sklearn import svm, preprocessing
from sklearn.model_selection import train_test_split

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
        log_state           = False

        self.config = scale_option, scale_mean, scale_std, predict_val, filename, log_state

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
                self.filename, self.log_state = self.config

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

        self.filename_text = QLabel()
        self.filename_text.setWordWrap(True)
        
        self.file_button = QPushButton(QC.translate('', 'Select model file'))
        self.file_button.clicked.connect(self.openFileNameDialog)

        
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
        self.conn_rest_layout.addWidget(self.filename_text)
        self.conn_rest_layout.addWidget(self.file_button)
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
        if self.filename:
            self.filename_text.setText(self.filename)

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
        filename            = self.filename
        log_state           = self.log_checkbox.isChecked()

        self.config = scale_option, scale_mean, scale_std, predict_val, filename, log_state
        
        self.addFunction(MLSVM_PredictFunction)

class MLSVM_PredictFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        logging.debug('MLSVM_PredictFunction::__init__() called')

    def execute(self, record):

        scale_option, scale_mean, scale_std, predict_val, filename, log_state = self.config
        b_open_succeeded = True

        if filename:
            try:
                with open(filename, 'rb') as f:
                    clf = pickle.load(f)
            except Exception as e:
                # not writeable?
                log_txt = '{SVM Predict}            Error opening model'
                record = None
                b_open_succeeded = False
        else:
            b_open_succeeded = False
            log_txt = '{SVM Predict}            No model file specified'

        if b_open_succeeded:
            if isinstance(record, (list, tuple, pd.DataFrame)):
                # scaling option only here available
                if not isinstance(record, pd.DataFrame):
                    record = pd.DataFrame(record)

                record = preprocessing.scale(record, with_mean=scale_mean, with_std=scale_std)
                record = clf.predict(record)
            elif record:
                # when only one value is passed
                predict_val = False
                record = pd.DataFrame([record])
                record = clf.predict([record])
            else:
                log_txt = '{SVM Predict}            No input specified'

                
            if predict_val:
                # predict only last value
                record = pd.DataFrame([record[-1]])
                record = clf.predict(record)

            log_txt = '{{SVM Predict}}            Predicted {} value'.format(len(record))

        result = Record(self.getPos(), (self.row +1, self.column), record,
                 log=log_state, log_txt=log_txt)
        
        return result
