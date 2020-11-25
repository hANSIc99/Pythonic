import sys, logging, pickle, datetime, os, signal, time, itertools, tty, termios, select
import multiprocessing as mp
import threading as mt
from element_types import Record
from PyQt5.QtCore import QCoreApplication, QObject, QThread, Qt, QTimer
from PyQt5.QtCore import pyqtSignal

"""
def target_0(instance, record, feed_pipe):

    element = instance(*record)
    ret = element.execute_ex(record)
    feed_pipe.send(ret)

    ## return element id und data
"""


class ProcessHandler(QThread):

    execComplete  = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject', name='execComplete')

    def __init__(self, element, inputdata):
        super().__init__()
        self.filename   = 'elements.' + element['Filename']
        self.id         = element['ID']
        self.config     = element['Config']
        self.mp         = element['Multiprocessing']
        self.inputData  = inputdata

        self.return_pipe, self.feed_pipe = mp.Pipe(duplex=False)

    def run(self):
        
        elementCls = getattr(__import__(self.filename, fromlist=['Element']), 'Element')
        element = elementCls("input", "config", self.feed_pipe)
        result = None

        if self.mp: ## attach Debugger if flag is set
            p_0 = mp.Process(target=element.execute)
            p_0.start()
        else:
            t_0 = mt.Thread(target=element.execute)
            t_0.start()

        # hier while loop wegen output
        result = Record(False, None, None)
        
        while not result.bComplete:
            result = self.return_pipe.recv()
            logging.debug('ProcessHandler::run() - intemerdiate result')


        self.execComplete.emit(self.id, "test2")
        logging.debug('ProcessHandler::run() - execution done')



class Operator(QThread):

    currentConfig = None

    def __init__(self,):
        super().__init__()

    def run(self):

        while True:
            time.sleep(1)
            #logging.debug('Operator::run() called')

    def startExec(self, id, config):
        self.currentConfig = config
        # https://stackoverflow.com/questions/34609935/passing-a-function-with-two-arguments-to-filter-in-python

        # return first element which matches the ID
        startElement = [x for x in config if x['ID'] == id][0]
        
        # register elements für den fall das alles gestoppt werden muss
        inputData = None
        runElement = ProcessHandler(startElement,inputData)
        runElement.execComplete.connect(self.execComplete)
        runElement.start()
        ## create processor and forward config and start filename
        logging.debug('Operator::startExec() called - id: 0x{:08x}'.format(id))

    def execComplete(self, id, data):

        logging.debug('Operator::execComplete() called - id: 0x{:08x}'.format(id))

