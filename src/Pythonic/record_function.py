from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox
import logging
from time import sleep
from datetime import datetime
from multiprocessing import Process
import os

# this object is switched between the elements and contains the targets and data
class Record():

    def __init__(self, source, target_0, record_0,
            target_1=None, record_1=None, log=False, log_txt=None, log_output=False):

        logging.debug('__init__() called Record')
        self.source   = source
        self.target_0 = target_0
        self.target_1 = target_1
        self.record_0 = record_0
        self.record_1 = record_1
        self.log = log
        self.log_txt = log_txt
        self.log_output = log_output
        self.pid = os.getpid()
    

    def __setstate__(self, state):
        logging.debug('__setstate__() called Record')
        self.source, self.target_0, self.target_1, \
            self.record_0, self.record_1, self.log, self.log_txt,\
            self.log_output, self.pid = state

    def __getstate__(self):
        logging.debug('__getstate__() called Record')
        return (self.source, self.target_0, self.target_1,
                self.record_0, self.record_1, self.log, self.log_txt,
                self.log_output, self.pid)


class Function():
    # baustelle: functionsträger
    # erstelle in execute einen neuen record

    def __init__(self, config, b_debug, row, column):

        self.config = config
        self.row = row
        self.column = column
        self.b_debug = b_debug
        logger = logging.getLogger()

    def __setstate__(self, state):
        logging.debug('__setstate__() called Function')
        self.config, self.b_debug, self.row, self.column = state

    def __getstate__(self):
        logging.debug('__getstate__() called Function')
        return (self.config, self.b_debug, self.row, self.column)

    def execute(self, record):
        logging.debug('execute() called Function')

        result = Record(self.getPos(), None, None, None)
        return result

    def getPos(self):
        
        return (self.row, self.column)


