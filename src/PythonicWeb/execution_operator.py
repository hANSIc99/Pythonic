import sys, logging, pickle, datetime, os, signal, time, itertools, tty, termios, select, queue
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

    execComplete  = Signal(object, object, object) # id, data, thread-identifier
    removeSelf    = Signal(object, object) # id, thread-identifier

    def __init__(self, element, inputdata, identifier):
        super().__init__()
        self.element    = element
        self.inputData  = inputdata
        self.identifier = identifier
        #self.pid        = None
        self.instance   = None


        self.queue      = None 


        self.finished.connect(self.done)

    def run(self):

        bMP = self.element['Config']['GeneralConfig']['MP']

        if bMP:
            self.queue = mp.Queue()
        else:
            self.queue = queue.Queue()

        elementCls = getattr(__import__('elements.' + self.element['Filename'], fromlist=['Element']), 'Element')
        self.instance = elementCls(self.element['Config'], self.inputData, self.queue)
        result = None

        

        if bMP: ## attach Debugger if flag is set
            self.p_0 = mp.Process(target=self.instance.execute)
            self.p_0.start()
            #self.pid = p_0.pid
        else:
            t_0 = mt.Thread(target=self.instance.execute)
            t_0.start()



        result = Record(False, None, None)
        
        ##################################################################
        #                                                                # 
        #                          MULTITHREADING                        #
        #                                                                #
        ##################################################################

        # Check if it is an intemediate result (result.bComplete)
        # or if the execution was stopped by the user (self.element.bStop)
                
        while not result.bComplete and not self.instance.bStop and not bMP:
            logging.debug("TEST")
            result = self.queue.get()
            self.execComplete.emit(self.element['Id'], result, self.identifier)
            logging.debug('ProcessHandler::run() - Multithreading: result received - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))


        ##################################################################
        #                                                                # 
        #                         MULTIPROCESSING                        #
        #                                                                #
        ##################################################################

        while bMP and self.p_0.is_alive():
            try:
                result = self.queue.get(block=True, timeout=0.2)
                self.execComplete.emit(self.element['Id'], result, self.identifier)
                logging.debug('ProcessHandler::run() - Multiprocessing: execution completed - id: 0x{:08x}, ident: {:04d}, pid: {}'.format(
                    self.element['Id'], self.identifier, self.p_0.pid))
            except queue.Empty:
                logging.debug('queue empty')
                pass
            
            


        logging.debug('ProcessHandler::run() - PROCESSING DONE - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        
    def stop(self):
        logging.debug('ProcessHandler::stop() - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        if self.element['Config']['GeneralConfig']['MP']:
            self.p_0.terminate()  
            self.p_0.join()
            x = 3     
        else:
            self.instance.bStop = True

    def done(self):
        logging.debug('ProcessHandler::done() removing Self - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        self.removeSelf.emit(self.element['Id'], self.identifier)
    


class Operator(QThread):

    currentConfig = None
    processHandles = {}
    updateElementStatus = Signal(object) # command

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
        runElement.execComplete.connect(self.operationDone)
        runElement.removeSelf.connect(self.removeOperatorThread)

        self.updateStatus(startElement, True)

        runElement.start()



        self.processHandles[identifier] = runElement
        

        logging.debug('Operator::startExec() called - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))

    def stopExec(self, id):
        logging.debug('Operator::stopExec() called - id: 0x{:08x}'.format(id))
        for threadIdentifier, processHandle in self.processHandles.items():
            if processHandle.element['Id'] == id:
                processHandle.stop()

    
    def updateStatus(self, element, status):
        #start highlight
        # area
        # id
        # target = "Element"
        # cmd = UpdateElementStatus
        
        address = {
            'target'    : 'Element',
            'area'      : element['GridNo'],
            'id'        : element['Id']              
        }
        
        cmd = { 
            'cmd'       : 'UpdateElementStatus',
            'address'   : address,
            'data'      : status
            }

        self.updateElementStatus.emit(cmd)


    def operationDone(self, id, record, identifier):

        #logging.debug('Operator::operationDone() called - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))
        if record.exit:
            logging.debug('Operator::operationDone() exit Message received - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))
        else:
            logging.debug('Operator::operationDone() result received - id: 0x{:08x}, ident: {:04d} data: {}'.format(id, identifier, record.data))

    def removeOperatorThread(self, id, identifier):

        logging.debug('Operator::removeOperatorThread() called - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))
        procHandle = self.processHandles[identifier]
        self.updateStatus(procHandle.element, False)
        procHandle.deleteLater()
        del self.processHandles[identifier]






