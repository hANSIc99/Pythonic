import sys, logging, pickle, datetime, os, signal, time, itertools, tty, termios, select
import multiprocessing as mp
from PyQt5.QtCore import QCoreApplication, QObject, QThread, Qt, QTimer
from PyQt5.QtCore import pyqtSignal


def target_0(function, record, feed_pipe):

    ret = function.execute_ex(record)
    feed_pipe.send(ret)

    ## return element id und data



class ProcessHandler(QThread):

    def __init__(self, filename, config):
        super().__init__()
        filename = 'elements.' + filename
        self.elementFunction = getattr(__import__(filename, fromlist=['Element']), 'Element')
        self.return_pipe, self.feed_pipe = mp.Pipe(duplex=False)
        #BAUSTELLE
        p_0 = mp.Process(target=target_0, args=(function, record, self.feed_pipe, ))
        logging.debug('check')

    def run(self):




        while True:
            time.sleep(1)
            logging.debug('Running element')



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
        runElement = ProcessHandler(startElement['Filename'], startElement['Config'])
        runElement.start()
        ## create processor and forward config and start filename
        logging.debug('Operator::startExec() called - id: {:08x}'.format(id))


