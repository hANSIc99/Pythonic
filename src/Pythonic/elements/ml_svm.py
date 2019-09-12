from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, pyqtSlot, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor, QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox, QStackedWidget, QFileDialog
from elementeditor import ElementEditor
from PyQt5.QtCore import QCoreApplication as QC
from pythonic_binance.client import Client
import pandas as pd
import os.path, datetime, logging, requests, json, pickle
from time import sleep
from Pythonic.record_function import Record, Function
from Pythonic.elementmaster import ElementMaster
from email.message import EmailMessage
from email.contentmanager import raw_data_manager
from sys import getsizeof
from sklearn import svm, preprocessing
from sklearn.model_selection import train_test_split
#from smtplib import SMTP

class MLSVM(ElementMaster):

    pixmap_path = 'images/MLSVM.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        # scale_option, scale_mean, scale_std train_eval, decision_function, gamma_mode, 
        #    gamma_value, filename, log_state

        
        scale_option        = 0
        scale_mean          = True
        scale_std           = True
        train_eval          = 2
        decision_function   = 0
        gamma_mode          = 0
        gamma_value         = '1.0'
        filename            = None
        log_state           = False

        self.config = scale_option, scale_mean, scale_std, train_eval, decision_function, \
                gamma_mode, gamma_value, filename, log_state

        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('MLSVM::__init__() called at row {}, column {}'.format(row, column))
        self.addFunction(MLSVMFunction)

    def __setstate__(self, state):
        logging.debug('MLSVM::__setstate__() called')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(MLSVMFunction)

    def __getstate__(self):
        logging.debug('MLSVM::__getstate__() called')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('MLSVM::openEditor() called')

    def edit(self):

        logging.debug('MLSVM::edit()')

        """
        gamma: auto oder float eingabe
        decision function shape: ovr oder ovo

        data split train / eval
        """
        self.scale_option, self.scale_mean, self.scale_std, self.train_eval, self.decision_function, \
                self.gamma_mode, self.gamma_value, self.filename, self.log_state = self.config

        self.scale_label = QLabel()
        self.scale_label.setText(QC.translate('', 'Scale n_samples ?'))
        self.scale_list = QComboBox()
        self.scale_list.addItem('No', QVariant(False))
        self.scale_list.addItem('Yes', QVariant(True))

        
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

        self.train_test_label = QLabel()
        self.train_test_label.setText(
                QC.translate('', 'Choose train / evalutaion ratio:'))

        self.train_test_list = QComboBox()
        self.train_test_list.addItem('90/10', QVariant(90))
        self.train_test_list.addItem('80/20', QVariant(80))
        self.train_test_list.addItem('70/30', QVariant(70))
        self.train_test_list.addItem('60/40', QVariant(60))
        self.train_test_list.addItem('50/50', QVariant(50))

        self.decision_function_label = QLabel()
        self.decision_function_label.setText(QC.translate('', 'Choose decision function shape:'))

        self.decision_function_list = QComboBox()
        self.decision_function_list.addItem('ovo', QVariant('ovo'))
        self.decision_function_list.addItem('ovr', QVariant('ovr'))

        self.gamma_label = QLabel()
        self.gamma_label.setText(QC.translate('', 'Gamma:'))

        self.gamma_list = QComboBox()
        self.gamma_list.addItem('Auto', QVariant('auto'))
        self.gamma_list.addItem('Scaled', QVariant('scaled'))
        self.gamma_list.addItem('Manual', QVariant('manual'))

        self.gamma_input_line = QWidget()
        self.gamma_input_line_layout = QHBoxLayout(self.gamma_input_line)
        self.gamma_input_txt = QLabel()
        self.gamma_input_txt.setText(QC.translate('', 'Gamma:'))
        self.gamma_input = QLineEdit()
        self.gamma_input.setPlaceholderText('1.0')
        self.gamma_input.setValidator(QDoubleValidator(0, 999, 3))
        self.gamma_input_line_layout.addWidget(self.gamma_input_txt)
        self.gamma_input_line_layout.addWidget(self.gamma_input)

        self.conn_rest_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.filename_text = QLabel()
        self.filename_text.setWordWrap(True)
        
        self.file_button = QPushButton(QC.translate('', 'Select model output file'))
        self.file_button.clicked.connect(self.ChooseFileDialog)

        
        """
        output: prediction quality
        """
        self.help_text_1 = QLabel()
        self.help_text_1.setText(QC.translate('', 'Expects a tuple (n_samples, n_features) as input.'))

        self.help_text_2 = QLabel()
        self.help_text_2.setText(QC.translate('', 'Outputs a contigency table in the format:'))
        self.help_text_3 = QLabel()
        self.help_text_3.setText(QC.translate('', '{\'TP\': 23, \'FP\': 13, \'FN\':12, \'TN\': 33}'))

        

        # hier logging option einfügen
        self.log_line = QWidget()
        self.ask_for_logging = QLabel()
        self.ask_for_logging.setText(QC.translate('', 'Log output?'))
        self.log_checkbox = QCheckBox()
        self.log_line_layout = QHBoxLayout(self.log_line)
        self.log_line_layout.addWidget(self.ask_for_logging)
        self.log_line_layout.addWidget(self.log_checkbox)
        self.log_line_layout.addStretch(1)

        
        self.ml_svm_edit = ElementEditor(self)
        self.ml_svm_edit.setWindowTitle(QC.translate('', 'Support Vector Machine'))
        self.ml_svm_edit.setMinimumHeight(600)

        # signals and slots
        self.gamma_list.currentIndexChanged.connect(self.gammaIndexChanged)
        self.scale_list.currentIndexChanged.connect(self.scaledIndexChanged)
        self.confirm_button.clicked.connect(self.ml_svm_edit.closeEvent)
        self.ml_svm_edit.window_closed.connect(self.edit_done)

        # load config
        self.loadLastConfig()

        self.conn_rest_layout.addWidget(self.help_text_1)
        self.conn_rest_layout.addWidget(self.scale_label) # scale: copy = false
        self.conn_rest_layout.addWidget(self.scale_list)
        self.conn_rest_layout.addWidget(self.scale_input_area)
        self.conn_rest_layout.addWidget(self.train_test_label)
        self.conn_rest_layout.addWidget(self.train_test_list)
        self.conn_rest_layout.addWidget(self.decision_function_label)
        self.conn_rest_layout.addWidget(self.decision_function_list)
        self.conn_rest_layout.addWidget(self.gamma_label)
        self.conn_rest_layout.addWidget(self.gamma_list)
        self.conn_rest_layout.addWidget(self.gamma_input_line)
        self.conn_rest_layout.addWidget(self.filename_text)
        self.conn_rest_layout.addWidget(self.file_button)
        self.conn_rest_layout.addStretch(1)
        self.conn_rest_layout.addWidget(self.help_text_2)
        self.conn_rest_layout.addWidget(self.help_text_3)
        self.conn_rest_layout.addWidget(self.log_line)
        self.conn_rest_layout.addWidget(self.confirm_button)
        self.ml_svm_edit.setLayout(self.conn_rest_layout)
        self.ml_svm_edit.show()

    def loadLastConfig(self):

        logging.debug('MLSVM::loadLastConfig() called')
        
        self.train_test_list.setCurrentIndex(self.train_eval)
        self.decision_function_list.setCurrentIndex(self.decision_function)
        self.gamma_list.setCurrentIndex(self.gamma_mode)
        self.gamma_input.setText('{}'.format(self.gamma_value))
        self.gammaIndexChanged(self.gamma_mode)
        self.scale_list.setCurrentIndex(self.scale_option)
        self.scaledIndexChanged(self.scale_option)
        self.scale_center_checkbox.setChecked(self.scale_mean)
        self.scale_std_checkbox.setChecked(self.scale_std)
        self.log_checkbox.setChecked(self.log_state)
        if self.filename:
            self.filename_text.setText(self.filename)

    def scaledIndexChanged(self, event):

        current_index = event
        logging.debug('MLSVM::scaledIndexChanged() called: {}'.format(event))
        if event == 1 :
            self.scale_input_area.setVisible(True)
        else:
            self.scale_input_area.setVisible(False)

    def gammaIndexChanged(self, event):

        current_index = event
        logging.debug('MLSVM::gammaIndexChanged() called: {}'.format(event))
        if event == 2 :
            self.gamma_input_line.setVisible(True)
        else:
            self.gamma_input_line.setVisible(False)

    def ChooseFileDialog(self, event):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, \
                QC.translate('', 'Choose file'),"","All Files (*);;Text Files (*.txt)", \
                options=options)
        if fileName:
            logging.debug('ChooseFileDialog() called with filename: {}'.format(fileName))
            self.filename = fileName
            self.filename_text.setText(self.filename)


    def edit_done(self):

        logging.debug('MLSVM::edit_done() called')
        # scale_option, scale_mean, scale_std train_eval, decision_function, gamma_mode, 
        #    gamma_value, filename, log_state

        scale_option        = self.scale_list.currentIndex()
        scale_mean          = self.scale_center_checkbox.isChecked()
        scale_std           = self.scale_std_checkbox.isChecked()
        train_eval          = self.train_test_list.currentIndex()
        decision_function   = self.decision_function_list.currentIndex()
        gamma_mode          = self.gamma_list.currentIndex()
        gamma_value         = float(self.gamma_input.text())
        filename            = self.filename
        log_state           = self.log_checkbox.isChecked()

        self.config = scale_option, scale_mean, scale_std, train_eval, decision_function, gamma_mode, \
                gamma_value, filename, log_state
        
        self.addFunction(MLSVMFunction)

class MLSVMFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        logging.debug('MLSVMFunction::__init__() called')

    def execute(self, record):

        scale_option, scale_mean, scale_std, train_eval, decision_function, \
                gamma_mode, gamma_value, filename, log_state = self.config

        # expect a tuple (Xdata, Ylabels) as input
        X, Y = record

        if scale_option == 1:
            # X, axis, with_mean, with_std, copy
            X = preprocessing.scale(X, 0, scale_mean, scale_std, False)

        if train_eval == 0: # 90/10
            test_share = 0.1
        elif train_eval == 1: # 80/20
            test_share = 0.2 
        elif train_eval == 2: # 70/30
            test_share = 0.3
        elif train_eval == 3: # 60/40  
            test_share = 0.4
        else: # 50/50
            test_share = 0.5

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_share)

        if decision_function == 0: # one vs. one
            dec_func_shape = 'ovo'
        else: # one vs. rest
            dec_func_shape = 'ovr' 

        if gamma_mode == 0: # auto
            gamma_arg = 'auto'
        elif gamma_mode == 1: #scaled
            gamma_arg = 'scaled'
        else: # manual
            gamma_arg = gamma_value


        clf = svm.SVC(decision_function_shape='ovr', gamma=gamma_arg)
        clf.fit(X_train, Y_train)

        Y_predicted = clf.predict(X_test)

        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for idx, Y_pre in enumerate(Y_predicted):
            if Y_pre == Y_test[idx]: # true positives or true negatives

                if Y_test[idx] != 0: # true positive
                    tp += 1
                else: #true negative
                    tn += 1

            else: #false positives or false negatives

                if Y_test[idx] != 0: # false positive
                    fp += 1
                else: # false negative
                    fn += 1


        log_txt = '{SVM}                    Successful trained'

        if filename:
            try:
                with open(filename, 'wb') as f:
                    pickle.dump(clf, f)
            except Exception as e:
                # not writeable?
                log_txt = '{SVM}                    Successful trained - Error writing model to HDD'

        

        record = {'tp': tp, 'tn':tn, 'fp':fp, 'fn':fn}

        result = Record(self.getPos(), (self.row +1, self.column), record,
                 log=log_state, log_txt=log_txt)

        
        return result
