
import sys, logging, pickle, datetime, os, signal, time, itertools, select, queue, signal
import json
import random
import multiprocessing as mp
import threading as mt
from pathlib import Path
from PySide2.QtCore import QCoreApplication, QObject, QThread, Qt, QTimer
from PySide2.QtCore import Signal

    
try:
    from element_types import Record, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, ProcCMD, GuiCMD

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
        self.instance   = None
        self.element['Config']['Identifier'] = self.identifier
        self.pid        = None
        self.queue      = None 


        self.finished.connect(self.done)

    def run(self):
        #logging.debug('ProcessHandler::run() -id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        bMP = self.element['Config']['GeneralConfig']['MP']
        

        if bMP:
            self.return_queue = mp.Queue()
            self.cmd_queue    = mp.Queue()
        else:
            self.return_queue = queue.Queue()
            self.cmd_queue    = queue.Queue()

        try:

            #executable = str(Path.home() / 'Pythonic' / 'executables' / ) + '.py'
            #elementCls = getattr(__import__('executables.' + self.element['Filename'], fromlist=['Element']), 'Element')
            elementCls = getattr(__import__(self.element['Filename'], fromlist=['Element']), 'Element')
            #logging.debug('ProcessHandler::run() - loading file - id: 0x{:08x}, ident: {:04d} - {}'.format(
            #    self.element['Id'], self.identifier, self.element['Filename']))
        except Exception as e:
            logging.debug('ProcessHandler::run() - Error loading file - id: 0x{:08x}, ident: {:04d} - {} Error: {}'.format(
                self.element['Id'], self.identifier, self.element['Filename'], e))
            return

        self.instance = elementCls(self.element['Config'], self.inputData, self.return_queue, self.cmd_queue)
        result = None

        

        if bMP: ## attach Debugger if flag is set
            self.p_0 = mp.Process(target=self.instance.execute)
            self.p_0.start()
            self.pid = self.p_0.pid
        else:
            self.t_0 = mt.Thread(target=self.instance.execute)
            self.t_0.start()



        result = Record(None, None)
        
        ##################################################################
        #                                                                # 
        #                          MULTITHREADING                        #
        #                                                                #
        ##################################################################

        # Check if it is an intemediate result (result.bComplete)
        # or if the execution was stopped by the user (self.element.bStop)
        
        while not bMP:

            try:
                # First: Check if there is somethin in the Queue
                result = self.return_queue.get(block=True, timeout=0.2)
                # Seconds: Forward the result (is present)
                self.execComplete.emit(self.element['Id'], result, self.identifier)
            except queue.Empty:
                #logging.debug('return_queue empty')
                pass
            # Thirs: Check if Thread is still alive
            if not self.t_0.is_alive():
                break

            #logging.debug('ProcessHandler::run() - Multithreading: result received - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))



        ##################################################################
        #                                                                # 
        #                         MULTIPROCESSING                        #
        #                                                                #
        ##################################################################

        while bMP:

            try:
                result = self.return_queue.get(block=True, timeout=0.2)
                self.execComplete.emit(self.element['Id'], result, self.identifier)

                #logging.debug('ProcessHandler::run() - Multiprocessing: execution completed - id: 0x{:08x}, ident: {:04d}, pid: {}'.format(
                #    self.element['Id'], self.identifier, self.p_0.pid))
            except queue.Empty:
                #logging.debug('return_queue empty')
                pass
            
            if not self.p_0.is_alive():
                break
            


        #logging.debug('ProcessHandler::run() - PROCESSING DONE - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        
    def stop(self):
        logging.debug('ProcessHandler::stop() - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        self.cmd_queue.put(ProcCMD(True))

    def done(self):
        #logging.debug('ProcessHandler::done() removing Self - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        self.removeSelf.emit(self.element['Id'], self.identifier)
    


class Operator(QThread):

    currentConfig   = None
    processHandles  = {}
    command         = Signal(object) # command

    def __init__(self,):
        super().__init__()

    def run(self):

        while True:
            time.sleep(1)

    def startExec(self, id, config):
        #logging.debug('Operator::startExec() called - id: 0x{:08x}'.format(id))
        ## create processor and forward config and start filename
        self.currentConfig = config
        # https://stackoverflow.com/questions/34609935/passing-a-function-with-two-arguments-to-filter-in-python

        # return first element which matches the ID
        startElement = [x for x in config if x['Id'] == id][0]

        self.createProcHandle(startElement)

    def createProcHandle(self, element):    
        #neue function

        # register elements für den fall das alles gestoppt werden muss
        inputData = None

        # creating a random identifier
        identifier = random.randint(0, 9999)
        runElement = ProcessHandler(element,inputData, identifier)
        runElement.execComplete.connect(self.operationDone)
        runElement.removeSelf.connect(self.removeOperatorThread)

        
        if element["HighlightState"]:
            self.updateStatus(element, True)
        

        runElement.start()

        self.processHandles[identifier] = runElement
        #logging.debug('Operator::createProcHandle() called - identifier: {:04d}'.format(identifier))

        

    def stopExec(self, id):
        logging.debug('Operator::stopExec() called - id: 0x{:08x}'.format(id))
        
        for threadIdentifier, processHandle in self.processHandles.items():
            if processHandle.element['Id'] == id:
                processHandle.stop()

    def stopAll(self):

        logging.debug('Operator::stopAll() called')
        logging.info('User command: Stop All')
        for threadIdentifier, processHandle in self.processHandles.items():
            processHandle.stop()

    def startAll(self, config):

        logging.debug('Operator::startAll() called')
        logging.info('User command: Start All')
        self.currentConfig = config
        
        startElements = [x for x in config if not x['Socket']]

        for startElement in startElements:

            processes = filter(lambda item: item[1].element['Id'] == startElement['Id'], self.processHandles.items())
            runningProcess = next(processes, None)

            if(runningProcess):
                logging.debug('Operator::startAll() -Element already running - {} - id: 0x{:08x}'.format(
                    runningProcess[1].element['ObjectName'], runningProcess[1].element['Id']))
                return
            else:
                logging.debug('Operator::startAll() -Element started - {} - id: 0x{:08x}'.format(
                   startElement['ObjectName'], startElement['Id']))
                self.createProcHandle(startElement)

    def killAll(self):
        
        logging.debug('Operator::killAll() called')
        logging.info('User command: Kill All Processes')   
        # Separate dict must be created because call to removerOperatorThreads
        # modifies self.processHandles

        processes = dict(filter(lambda item: item[1].pid, self.processHandles.items())) 
        
        for threadIdentifier, processHandle in processes.items():
            os.kill(processHandle.pid, signal.SIGTERM)
            # removeOperatorThread is called in run() function of ProcessHandler
        

    def getElementStates(self):
        
        logging.debug('Operator::getElementStates() called')

        for threadIdentifier, processHandle in self.processHandles.items():
            #logging.debug('running elements: 0x{:08x}'.format(processHandle.element['Id']))
            self.updateStatus(processHandle.element, True)

        #if procHandle.element["HighlightState"]:
        #    self.updateStatus(procHandle.element, False)

    def updateStatus(self, element, status):
        #start highlight
        # area
        # id
        # target = "Element"
        # cmd = UpdateElementStatus
        logging.debug('Operator::updateStatus() called - {} - id: 0x{:08x}'.format(status, element['Id']))
        address = {
            'target'    : 'Element',
            'area'      : element['AreaNo'],
            'id'        : element['Id']              
        }
        
        cmd = { 
            'cmd'       : 'UpdateElementStatus',
            'address'   : address,
            'data'      : status
            }

        self.command.emit(cmd)

    def highlightConnection(self, parentId, childId, wrkArea):

        #logging.debug('Operator::updateStatus() called - {} - id: 0x{:08x}'.format(status, element['Id']))
        address = {
            'target'    : 'WorkingArea',
            'area'      : wrkArea           
        }

        data = {
            'parentId'  : parentId,
            'childId'   : childId
        }
        
        cmd = { 
            'cmd'       : 'HighlightConnection',
            'address'   : address,
            'data'      : data
            }

        self.command.emit(cmd)

    def operationDone(self, id, record, identifier):

        #logging.debug('Operator::operationDone() result received - id: 0x{:08x}, ident: {:04d} data: {}'.format(id, identifier, record.data))

        if isinstance(record, GuiCMD):
            #logging.info(record.text)
            address = {
                'target'    : 'Element',  
                'id'        : id                      
            }
            cmd = { 
                'cmd'       : 'ElementText',
                'address'   : address,
                'data'      : record.text
            }
            self.command.emit(cmd)
            return


        cfgElement = [x for x in self.currentConfig if x['Id'] == id][0]

        if cfgElement['Config']['GeneralConfig']['Logging'] and record.message:
            logging.info('{} - {}'.format(cfgElement['ObjectName'], record.message))

            data = {
                'Id'        : cfgElement['Id'],
                'ObjectName': cfgElement['ObjectName'],
                'Message'   : record.message
            }
            address = {
                'target'    : 'MainWindow',                        
            }
            cmd = { 
                'cmd'       : 'ElementMessage',
                'address'   : address,
                'data'      : data
            }
            self.command.emit(cmd)


        if cfgElement['Config']['GeneralConfig']['Debug'] :

            data = {
                'Id'        : cfgElement['Id'],
                'AreaNo'    : cfgElement['AreaNo'],
                'ObjectName': cfgElement['ObjectName'],
                'Output'    : str(record.data) 
            }
            address = {
                'target'    : 'MainWindow',                        
            }
            cmd = { 
                'cmd'       : 'DebugOutput',
                'address'   : address,
                'data'      : data
            }
            self.command.emit(cmd)


        # return if the element has no childs
        if not cfgElement['Childs']:
            return
        
        for childId in cfgElement['Childs']:
            childElement = [x for x in self.currentConfig if x['Id'] == childId][0]
            self.createProcHandle(childElement)
            self.highlightConnection(parentId=id, childId=childId, wrkArea=childElement['AreaNo'])

    def removeOperatorThread(self, id, identifier):

        logging.debug('Operator::removeOperatorThread() called - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))
        procHandle = self.processHandles[identifier]
        
        if procHandle.element["HighlightState"]:
            self.updateStatus(procHandle.element, False)
        
        procHandle.deleteLater()
        del self.processHandles[identifier]






