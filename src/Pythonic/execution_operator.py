
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


class ProcessHandler(QRunnable):

    execComplete  = Signal(object, object, object) # id, data, thread-identifier
    removeSelf    = Signal(object, object) # id, thread-identifier

    def __init__(self, element, inputdata, identifier, operator):
        super(ProcessHandler, self).__init__(self)

        self.element    = element
        self.inputData  = inputdata
        self.identifier = identifier
        self.instance   = None
        self.pid        = None
        self.queue      = None 
        self.operator   = operator
        self.element['Config']['Identifier'] = self.identifier


    def run(self):
        logging.debug('ProcessHandler::run() -id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))


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



        while not bMP:

            try:
                # First: Check if there is somethin in the Queue
                result = self.return_queue.get(block=True, timeout=0.2)
                # Seconds: Forward the result (is present)
                self.operator.operationDone(self.element['Id'], result, self.identifier)
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

                self.operator.operationDone(self.element['Id'], result, self.identifier)
                #logging.debug('ProcessHandler::run() - Multiprocessing: execution completed - id: 0x{:08x}, ident: {:04d}, pid: {}'.format(
                #    self.element['Id'], self.identifier, self.p_0.pid))
            except queue.Empty:
                #logging.debug('return_queue empty')
                pass
            
            if not self.p_0.is_alive():
                break
            
        self.operator.removeOperatorThread(self.element['Id'], self.identifier)
        
    def stop(self):
        logging.debug('ProcessHandler::stop() - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        self.cmd_queue.put(ProcCMD(True))


# https://forum.qt.io/topic/112731/super-in-python/2
# https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/



class OperatorStartAll(QRunnable): # AENDERN
    

    def __init__(self, operator):
        super(OperatorStartAll, self).__init__()
        self.operator       = operator
        self.setAutoDelete(False)
        
    def run(self):

        logging.debug('OperatorStartAll::startAll() called')
            
        startElements = [x for x in self.operator.currentConfig if not x['Socket']]

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
                self.operator.createProcHandle(startElement)


class OperatorElementOpDone(QRunnable):

    def __init__(self, config, id, record, identifier, operator):
        super(OperatorElementOpDone, self).__init__()


        self.currentConfig  = config
        self.id             = id
        self.record         = record
        self.identifier     = identifier
        self.operator       = operator


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

            self.operator.emitCommand(cmd)


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

            self.operator.emitCommand(cmd)

        # return if the element has no childs
        if not cfgElement['Childs']:
            return
        
        for childId in cfgElement['Childs']:
            childElement = [x for x in self.currentConfig if x['Id'] == childId][0]
            self.operator.createProcHandle(childElement)
            self.operator.highlightConnection(self.id, childId, childElement['AreaNo'])


class OperatorCreateProcHandle(QRunnable):
    
    def __init__(self, element, inputData, operator):
        super(OperatorCreateProcHandle, self).__init__()
        self.element    = element
        self.inputData  = inputData
        self.operator   = operator

    def run(self):


        identifier = self.operator.getIdent()
        runElement = ProcessHandler(self.element, self.inputData, identifier, self.operator)
        #runElement.signals.execComplete.connect(self.operator.operationDone)
        #runElement.signals.removeSelf.connect(self.operator.removeOperatorThread)

        if self.element["HighlightState"]: 
            self.operator.updateStatus(self.element, True)
        
        self.operator.addHandle(identifier, runElement)
        self.operator.threadpool.start(runElement)
        
        logging.info('Operator::createProcHandle() called - identifier: {:04d}'.format(identifier))


class Operator(QObject):

    currentConfig   = None
    processHandles  = {}
    command         = Signal(object) # command

    def __init__(self):
        super(Operator, self).__init__()

        self.threadpool         = QThreadPool.globalInstance()
        self.procHandleMutex    = QMutex()

        self._startAll          = OperatorStartAll(self)

        self.identGenMutex      = QMutex()
        self.n_ident            = 0

        self.updateStateMutex   = QMutex()
        self.operationDoneMutex = QMutex()

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

    def getIdent(self):

        self.identGenMutex.lock()
        self.n_ident += 1

        if not self.n_ident & 0x7fff:
            self.n_ident = 0
        self.identGenMutex.unlock()
        return self.n_ident


    def startExec(self, id, config):
        #logging.debug('Operator::startExec() called - id: 0x{:08x}'.format(id))
        ## create processor and forward config and start filename

        self.currentConfig = config
        # https://stackoverflow.com/questions/34609935/passing-a-function-with-two-arguments-to-filter-in-python

        # return first element which matches the ID
        startElement = [x for x in config if x['Id'] == id][0]

        self.createProcHandle(startElement)

    def createProcHandle(self, element, inputData=None):    
        #neue function
        procHandle = OperatorCreateProcHandle(element, inputData, self)

        #procHandle.signals.updateStatus.connect(self.updateStatus)
        #procHandle.signals.addHandle.connect(self.addHandle)
        self.threadpool.start(procHandle)    

    def addHandle(self, identifier, handle):
        
        self.procHandleMutex.lock()
        self.processHandles[identifier] = handle
        self.procHandleMutex.unlock()

    def stopExec(self, id):
        logging.debug('Operator::stopExec() called - id: 0x{:08x}'.format(id))
        # TODO MULTUTHREADING
        self.procHandleMutex.lock()
        for threadIdentifier, processHandle in self.processHandles.items():
            if processHandle.element['Id'] == id:
                processHandle.stop()
        self.procHandleMutex.unlock()

    def stopAll(self):

        logging.debug('Operator::stopAll() called')
        logging.info('User command: Stop All')
        self.procHandleMutex.lock()
        for threadIdentifier, processHandle in self.processHandles.items():
            processHandle.stop()
        self.procHandleMutex.unlock()

    def startAll(self, config):

        logging.info('User command: Start All')
        self.currentConfig              = config
        self.threadpool.start(self._startAll)

    def killAll(self):
        
        logging.debug('Operator::killAll() called')
        logging.info('User command: Kill All Processes')   
        # Separate dict must be created because call to removerOperatorThreads
        # modifies self.processHandles
        self.procHandleMutex.lock()
        processes = dict(filter(lambda item: item[1].pid, self.processHandles.items())) 
        self.procHandleMutex.unlock()
        for threadIdentifier, processHandle in processes.items():
            os.kill(processHandle.pid, signal.SIGTERM)
            # removeOperatorThread is called in run() function of ProcessHandler
        
    def getElementStates(self):
        
        logging.debug('Operator::getElementStates() called')
        self.procHandleMutex.lock()
        for threadIdentifier, processHandle in self.processHandles.items():
            #logging.debug('running elements: 0x{:08x}'.format(processHandle.element['Id']))
            self.updateStatus(processHandle.element, True)
        self.procHandleMutex.unlock()
        #if procHandle.element["HighlightState"]:
        #    self.updateStatus(procHandle.element, False)

    def updateStatus(self, element, status):
        #start highlight
        # area
        # id
        # target = "Element"
        # cmd = UpdateElementStatus
        #logging.debug('Operator::updateStatus() called - {} - id: 0x{:08x}'.format(status, element['Id']))
        self.updateStateMutex.lock()
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
        self.updateStateMutex.unlock()

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
        #self.operationDoneMutex.lock()
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
            self.operationDoneMutex.unlock()
            return
        
        operationDoneRunnable = OperatorElementOpDone(self.currentConfig, id, record, identifier, self)

        self.threadpool.start(operationDoneRunnable)
        #self.operationDoneMutex.unlock()
        
    def removeOperatorThread(self, id, identifier):
        
        logging.info('Operator::removeOperatorThread() called - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))

        self.procHandleMutex.lock()
        procHandle = self.processHandles[identifier]
        if procHandle.element["HighlightState"]:
            self.updateStatus(procHandle.element, False)

        del self.processHandles[identifier]

        self.procHandleMutex.unlock()
        
        






