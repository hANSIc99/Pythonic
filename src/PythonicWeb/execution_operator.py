import sys, logging, pickle, datetime, os, signal, time, itertools, tty, termios, select
import json
import random
import multiprocessing as mp
import threading as mt
from element_types import Record
from PySide2.QtCore import QCoreApplication, QObject, QThread, Qt, QTimer
from PySide2.QtCore import Signal

"""
def target_0(instance, record, feed_pipe):

    element = instance(*record)
    ret = element.execute_ex(record)
    feed_pipe.send(ret)

    ## return element id und data
"""


class ProcessHandler(QThread):

    execComplete  = Signal(object, object, object)

    def __init__(self, element, inputdata, identifier):
        super().__init__()
        self.filename   = 'elements.' + element['Filename']
        self.id         = element['Id']
        self.config     = element['Config']
        self.mp         = element['Multiprocessing']
        self.inputData  = inputdata
        self.identifier = identifier

        self.return_pipe, self.feed_pipe = mp.Pipe(duplex=False)

        self.finished.connect(self.done)

    def run(self):
        
        elementCls = getattr(__import__(self.filename, fromlist=['Element']), 'Element')
        element = elementCls(self.config, self.inputData, self.feed_pipe)
        result = None

        if self.mp: ## attach Debugger if flag is set
            p_0 = mp.Process(target=element.execute)
            p_0.start()
        else:
            t_0 = mt.Thread(target=element.execute)
            t_0.start()


        result = Record(False, None, None)
        
        
        
        # Check if it is an intemediate result
                
        while not result.bComplete:
            result = self.return_pipe.recv()
            # BAUSTELLE: Forward result
            logging.debug('ProcessHandler::run() - intemerdiate result - execution done - id: 0x{:08x}, ident: {:04d}'.format(self.id, self.identifier))


        logging.debug('ProcessHandler::run() - execution done - id: 0x{:08x}, ident: {:04d}'.format(self.id, self.identifier))

    def done(self):
        logging.debug('ProcessHandler::done() - execution done - id: 0x{:08x}, ident: {:04d}'.format(self.id, self.identifier))
        self.execComplete.emit(self.id, "test2", self.identifier)


class Operator(QThread):

    currentConfig = None
    processHandles = {}

    def __init__(self,):
        super().__init__()

    def run(self):

        while True:
            time.sleep(1)

    def startExec(self, id, config):
        logging.debug('Operator::startExec() bla')
        ## create processor and forward config and start filename
        self.currentConfig = config
        # https://stackoverflow.com/questions/34609935/passing-a-function-with-two-arguments-to-filter-in-python

        # return first element which matches the ID
        startElement = [x for x in config if x['Id'] == id][0]
        
        # register elements für den fall das alles gestoppt werden muss
        inputData = None

        # creating a random identifier
        identifier = random.randint(0, 9999)
        runElement = ProcessHandler(startElement,inputData, identifier)
        runElement.execComplete.connect(self.execComplete)
        #runElement.finished.connect
        runElement.start()
        self.processHandles[identifier] = runElement
        

        logging.debug('Operator::startExec() called - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))

    def execComplete(self, id, data, identifier):

        logging.debug('Operator::execComplete() called - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))
        # remove processHandle from dict
        qobject = self.processHandles[identifier]
        qobject.deleteLater()
        del self.processHandles[identifier]

