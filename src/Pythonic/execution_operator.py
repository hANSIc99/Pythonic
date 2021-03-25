
import sys, logging, pickle, datetime, os, signal, time, itertools, select, queue, signal
import json
import random
import multiprocessing as mp
import threading as mt
from importlib import reload
from pathlib import Path
from PySide2.QtCore import QCoreApplication, QObject, QThread, Qt, QRunnable, QThreadPool, QMutex
from PySide2.QtCore import Signal





try:
    from element_types import Record, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, ProcCMD, GuiCMD

class ProcessHandlerSignal(QObject):

    execComplete    = Signal(int, object, int) 
    removeSelf      = Signal(int, int) # id, thread-identifier

    def __init__(self, parent=None):
        super(ProcessHandlerSignal, self).__init__(parent)
        self.parent = parent

class ProcessHandler(QRunnable):

    execComplete  = Signal(object, object, object) # id, data, thread-identifier
    removeSelf    = Signal(object, object) # id, thread-identifier

    def __init__(self, element, inputdata, identifier):
        #super().__init__()
        super(ProcessHandler, self).__init__(self)
        #self.parent     = parent
        self.element    = element
        self.inputData  = inputdata
        self.identifier = identifier
        self.instance   = None
        self.pid        = None
        self.queue      = None 
        self.element['Config']['Identifier'] = self.identifier
        #self.finished.connect(self.done)
        self.signals    = ProcessHandlerSignal()
        self.setAutoDelete(True)

    def run(self):
        logging.debug('ProcessHandler::run() -id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))

        """
        def finished():
            self.removeSelf.emit(self.element['Id'], self.identifier)
            #self.deleteLater()
        """
        #self.finished.connect(finished)  
        
        

        bMP = self.element['Config']['GeneralConfig']['MP']

        if bMP:
            self.return_queue = mp.Queue()
            self.cmd_queue    = mp.Queue()
        else:
            self.return_queue = queue.Queue()
            self.cmd_queue    = queue.Queue()

        try:

            # This affects only first invocation
            module = __import__(self.element['Filename'])
            #logging.warning("Load module first time")
            
            # Reload to execute possible changes
            module = reload(module) 

            elementCls = getattr(module, 'Element')

        except Exception as e:
            logging.warning('ProcessHandler::run() - Error loading file - id: 0x{:08x}, ident: {:04d} - {} Error: {}'.format(
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

        """
        recordDone = Record(2, 'Sending value of cnt: x')
        self.signals.execComplete.emit(self.element['Id'], recordDone, self.identifier)
        self.signals.removeSelf.emit(self.element['Id'], self.identifier)

        return
        """


        while not bMP:

            try:
                # First: Check if there is somethin in the Queue
                result = self.return_queue.get(block=True, timeout=0.2)
                # Seconds: Forward the result (is present)
                self.signals.execComplete.emit(self.element['Id'], result, self.identifier)
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
                self.signals.execComplete.emit(self.element['Id'], result, self.identifier)

                #logging.debug('ProcessHandler::run() - Multiprocessing: execution completed - id: 0x{:08x}, ident: {:04d}, pid: {}'.format(
                #    self.element['Id'], self.identifier, self.p_0.pid))
            except queue.Empty:
                #logging.debug('return_queue empty')
                pass
            
            if not self.p_0.is_alive():
                break
            


        logging.debug('ProcessHandler::run() - PROCESSING DONE - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        
    def stop(self):
        logging.debug('ProcessHandler::stop() - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        self.cmd_queue.put(ProcCMD(True))

    def done(self):
        #logging.info('ProcessHandler::done() removing Self - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        self.removeSelf.emit(self.element['Id'], self.identifier)
    


# https://forum.qt.io/topic/112731/super-in-python/2
# https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/



class OperatorStartAll(QThread):
    
    createProcHandle = Signal(object) # command

    def __init__(self):
        super(OperatorStartAll, self).__init__()
        self.currentConfig  = None
        self.processHandles = {}
        
        

    def run(self):

        logging.debug('OperatorStartAll::startAll() called')
            
        startElements = [x for x in self.currentConfig if not x['Socket']]

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
                
                self.createProcHandle.emit(startElement)
        
class WorkerSignalOpDone(QObject):

    command             = Signal(object)
    createProcHandle    = Signal(object)
    highlightConnection = Signal(int, int, int) 

    def __init__(self, parent=None):
        super(WorkerSignalOpDone, self).__init__(parent)
        self.parent = parent

class OperatorElementOpDone(QRunnable):

    def __init__(self, config, id, record, identifier):
        super(OperatorElementOpDone, self).__init__()
        #self.parent = parent



        self.signals = WorkerSignalOpDone(self) 

        self.currentConfig  = config
        self.id             = id
        self.record         = record
        self.identifier     = identifier

        self.setAutoDelete(True)

    def run(self):

        logging.debug("OperatorElementOpDone::run() called")

        cfgElement = [x for x in self.currentConfig if x['Id'] == self.id][0]

        if cfgElement['Config']['GeneralConfig']['Logging'] and self.record.message:
            logging.info('{} - {}'.format(cfgElement['ObjectName'], self.record.message))

            data = {
                'Id'        : cfgElement['Id'],
                'ObjectName': cfgElement['ObjectName'],
                'Message'   : self.record.message
            }
            address = {
                'target'    : 'MainWindow',                        
            }
            cmd = { 
                'cmd'       : 'ElementMessage',
                'address'   : address,
                'data'      : data
            }
            self.signals.command.emit(cmd)


        if cfgElement['Config']['GeneralConfig']['Debug'] :

            data = {
                'Id'        : cfgElement['Id'],
                'AreaNo'    : cfgElement['AreaNo'],
                'ObjectName': cfgElement['ObjectName'],
                'Output'    : str(self.record.data) 
            }
            address = {
                'target'    : 'MainWindow',                        
            }
            cmd = { 
                'cmd'       : 'DebugOutput',
                'address'   : address,
                'data'      : data
            }
            self.signals.command.emit(cmd)


        # return if the element has no childs
        if not cfgElement['Childs']:
            return
        
        for childId in cfgElement['Childs']:
            childElement = [x for x in self.currentConfig if x['Id'] == childId][0]
            self.signals.createProcHandle.emit(childElement)
            self.signals.highlightConnection.emit(self.id, childId, childElement['AreaNo'])

class Operator(QObject):

    currentConfig   = None
    processHandles  = {}
    command         = Signal(object) # command

    def __init__(self):
        super(Operator, self).__init__()

        self.threadpool = QThreadPool.globalInstance()
        self._startAll  = OperatorStartAll()
        self._startAll.createProcHandle.connect(self.createProcHandle) 

    def start(self, config):

        # check for autostart elements
        logging.debug('Operator::start() called')

        if not config: # return here when there is no config file
            return

        self.currentConfig = config

        startElements = [x for x in self.currentConfig if not x['Socket'] and x['Config']['GeneralConfig']['Autostart']]

        for startElement in startElements:
            logging.info("Autostart " + startElement['ObjectName'])
            self.createProcHandle(startElement)

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
        runElement = ProcessHandler(element, inputData, identifier)
        runElement.signals.execComplete.connect(self.operationDone)
        #runElement.signals.removeSelf.connect(self.removeOperatorThread)
        #runElement.removeSelf.connect(self.removeOperatorThread)

        """
        if element["HighlightState"]: ## MEMORY LEAK
            self.updateStatus(element, True)
        """
        self.threadpool.start(runElement)
        #runElement.start()
        
        #self.processHandles[identifier] = runElement
        #logging.info('Operator::createProcHandle() called - identifier: {:04d}'.format(identifier))
    

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

        logging.info('User command: Start All')
        self.currentConfig              = config
        self._startAll.currentConfig    = config
        self._startAll.processHandles   = self.processHandles

        self._startAll.start()

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
        #logging.debug('Operator::updateStatus() called - {} - id: 0x{:08x}'.format(status, element['Id']))
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

        #self.command.emit(cmd)

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

    def emitCommand(self, command):

        self.command.emit(command)

    def operationDone(self, id, record, identifier):

        #logging.info('Operator::operationDone() result received - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))
        
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
        """
        operationDoneRunnable = OperatorElementOpDone(self.currentConfig, id, record, identifier)
        operationDoneRunnable.signals.command.connect(self.emitCommand)
        operationDoneRunnable.signals.createProcHandle.connect(self.createProcHandle)
        operationDoneRunnable.signals.highlightConnection.connect(self.highlightConnection)

        self.threadpool.start(operationDoneRunnable)
        """

        
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
        """
        logging.debug('Operator::removeOperatorThread() called - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))
        procHandle = self.processHandles[identifier]
        """
        
        startElement = [x for x in self.currentConfig if x['Id'] == id][0]
        self.updateStatus(startElement, False)
        """
        if procHandle.element["HighlightState"]:
            self.updateStatus(procHandle.element, False)
        """
        """
        procHandle.deleteLater()
        del self.processHandles[identifier]
        """





