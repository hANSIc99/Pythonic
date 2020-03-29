import logging
import os

import time

alphabet = { 0 : 'A', 1 : 'B', 2 : 'C', 3 : 'D', 4 : 'E', 5 : 'F', 6 : 'G', 7 : 'H', 8 : 'J',
        9 : 'K', 10 : 'L', 11 : 'M', 12 : 'N', 13 : 'O', 14 : 'P', 15 : 'Q', 16 : 'R', 17 : 'S',
        18 : 'T', 19 : 'U', 20 : 'V', 21 : 'W', 22 : 'X', 23 : 'Y', 24 : 'Z'}

# this object is switched between the elements and contains the targets and data
class Record():

    def __init__(self, source, target_0, record_0,
            target_1=None, record_1=None, log=False, log_txt=None):

        logging.debug('__init__() called Record')
        self.source   = source
        self.target_0 = target_0
        self.target_1 = target_1
        self.record_0 = record_0
        self.record_1 = record_1
        self.log = log
        self.log_txt = log_txt
        #self.log_output = log_output
        self.pid = os.getpid()
    

    def __setstate__(self, state):
        logging.debug('__setstate__() called Record')
        self.source, self.target_0, self.target_1, \
            self.record_0, self.record_1, self.log, self.log_txt,\
            self.pid = state

    def __getstate__(self):
        logging.debug('__getstate__() called Record')
        return (self.source, self.target_0, self.target_1,
                self.record_0, self.record_1, self.log, self.log_txt,
                self.pid)

class PipeRecord():

    def __init__(self, source, pid, target_0, record_0):
        self.source = source
        self.pid = pid
        self.target_0 = target_0
        self.record_0 = record_0

    def __setstate__(self, state):
        logging.debug('__setstate__() called PipeRecord')
        self.source, self.pid, self.target_0, self.record_0 = state

    def __getstate__(self):
        logging.debug('__getstate__() called PipeRecord')
        return (self.source, self.pid, self.target_0, self.record_0)


class Function():

    def __init__(self, config, b_debug, row, column):
        logging.debug('Function.__init__()')
        self.config = config
        self.row = row
        self.column = column
        self.b_debug = b_debug
        self.pid = 0
        logger = logging.getLogger()

    def __setstate__(self, state):
        logging.debug('__setstate__() called Function')
        self.config, self.b_debug, self.row, self.column, self.pid = state

    def __getstate__(self):
        logging.debug('__getstate__() called Function')
        return (self.config, self.b_debug, self.row, self.column, self.pid)

    def getSig(self):
        return self.fire

    def execute_ex(self, record, callback):

        logging.debug('execute_ex() called Function')
        self.callback = callback

        """
        while True:
            #self.callback = self.pid
            self.callback = 'hey'
            time.sleep(3)
        """

        try:
            result =self.execute(record)
        except Exception as e:
            result = Record(self.getPos(), None, e, None)

        return result

    def execute(self, record):
        logging.debug('execute() called Function')

        result = Record(self.getPos(), None, None, None)
        return result

    def getPos(self):
        
        return (self.row, self.column)


