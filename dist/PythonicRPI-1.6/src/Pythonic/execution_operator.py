
import sys, logging, pickle, datetime, os, signal, time, itertools, select, queue, signal
import json
import random
import multiprocessing as mp
import threading as mt
from importlib import reload
from pathlib import Path
from PySide2.QtCore import QCoreApplication, QObject, QThread, Qt, QRunnable, QThreadPool, QMutex, Signal


try:
    from element_types import Record, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, ProcCMD, GuiCMD



class ProcessHandler(QRunnable):

    def __init__(self, element, inputdata, identifier, operator):
        super(ProcessHandler, self).__init__()

        self.element    = element
        self.inputData  = inputdata
        self.identifier = identifier
        self.instance   = None
        self.pid        = None
        self.queue      = None 
        self.operator   = operator
        self.element['Config']['Identifier'] = self.identifier

        logging.debug('ProcessHandler::__init__() called') 


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

        self.instance = elementCls(self.element['Id'], self.element['Config'], self.inputData, self.return_queue, self.cmd_queue)
        result = None

        

        if bMP: ## attach Debugger if flag is set
            self.p_0 = mp.Process(target=self.instance.execute_ex)
            self.p_0.start()
            self.pid = self.p_0.pid
        else:
            self.t_0 = mt.Thread(target=self.instance.execute_ex)
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
                self.operator.operationDone(self.element['Id'], self.element['AreaNo'], result, self.identifier)
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

                self.operator.operationDone(self.element['Id'], self.element['AreaNo'], result, self.identifier)
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
        self.cmd_queue.put(ProcCMD(None, True))

    def feed(self, data): 
        logging.debug('ProcessHandler::feed() - id: 0x{:08x}, ident: {:04d}'.format(self.element['Id'], self.identifier))
        """
        if isinstance(data, ProcCMD):
            self.cmd_queue.put(data)
        else:
        """
        self.cmd_queue.put(ProcCMD(data))

class OperatorStartAll(QRunnable):
    

    def __init__(self, operator):
        super(OperatorStartAll, self).__init__()
        self.operator       = operator
        self.setAutoDelete(False)
        
    def run(self):

        logging.debug('OperatorStartAll::startAll() called')
            
        startElements = [x for x in self.operator.currentConfig if not x['Socket']]

        for startElement in startElements:
            
            
            processes = filter(lambda item: item[1].element['Id'] == startElement['Id'], self.operator.processHandles.items())
            runningProcess = next(processes, None)

            if(runningProcess):
                logging.debug('Operator::startAll() -Element already running - {} - id: 0x{:08x}'.format(
                    runningProcess[1].element['ObjectName'], runningProcess[1].element['Id']))
                return
            else:
                logging.debug('Operator::startAll() -Element started - {} - id: 0x{:08x}'.format(
                   startElement['ObjectName'], startElement['Id']))
                
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
            self.operator.createProcHandle(childElement, self.record.data)
            self.operator.highlightConnection(self.id, childId, childElement['AreaNo'])

class OperatorCreateProcHandle(QRunnable):
    
    def __init__(self, element, inputData, procHandles, operator):
        super(OperatorCreateProcHandle, self).__init__()
        self.element        = element
        self.inputData      = inputData
        self.procHandles    = procHandles
        self.operator       = operator

    def run(self):

        # check if inputData is a Stop command
        bStop = False
        if isinstance(self.inputData, ProcCMD):
            bStop = self.inputData.bStop



        # Check if an already running element has to be stopped
        if self.element['AllowStream'] or bStop:
            
            runningInstance =  list(filter(lambda item: item[1].element['Id'] == self.element['Id'], self.procHandles.items())) 
            # when runningInstance contains an element forward input data to it
            if runningInstance:
                # [0] first element in the list, [1] ProcessHandler
                tagetProc = runningInstance[0][1]

                if not bStop:
                    tagetProc.feed(self.inputData)
                else:
                    tagetProc.stop() # Send Stop command to running process

                return


        # return here if inputData is a Stop command
        if bStop:
            return

        identifier = self.operator.getIdent()
        runElement = ProcessHandler(self.element, self.inputData, identifier, self.operator)

        if self.element["HighlightState"]: 
            self.operator.updateStatus(self.element, True)
        
        self.operator.addHandle(identifier, runElement)
        self.operator.threadpool.start(runElement)
        
        logging.debug('Operator::createProcHandle() called - identifier: {:04d}'.format(identifier))

class OperatorReturnElementState(QRunnable):

    def __init__(self, processHandles, operator):
        super(OperatorReturnElementState, self).__init__()
        self.processHandles = processHandles
        self.operator       = operator

    def run(self):

        for threadIdentifier, processHandle in self.processHandles.items():
            #logging.debug('running elements: 0x{:08x}'.format(processHandle.element['Id']))
            self.operator.updateStatus(processHandle.element, True)

class OperatorStopExec(QRunnable):

    def __init__(self, processHandles, id, operator):
        super(OperatorStopExec, self).__init__()
        self.processHandles = processHandles
        self.operator       = operator
        self.id             = id

    def run(self):

        for threadIdentifier, processHandle in self.processHandles.items():
            if processHandle.element['Id'] == self.id:
                processHandle.stop()

class Operator(QObject):

    currentConfig   = None
    processHandles  = {}
    command         = Signal(object) # command

    def __init__(self):
        super(Operator, self).__init__()


        logging.debug('Operator::__init__() called')
        self.threadpool         = QThreadPool.globalInstance()
        self.procHandleMutex    = QMutex()

        self._startAll          = OperatorStartAll(self)

        self.identGenMutex      = QMutex()
        self.n_ident            = 0


    def start(self, config):

        logging.info('<#>DAEMON STARTED<#>')

        if not config: # return here when there is no config file
            return

        self.currentConfig = config

        # check for autostart elements

        startElements = [x for x in self.currentConfig if not x['Socket'] and x['Config']['GeneralConfig']['Autostart']]

        for startElement in startElements:
            logging.info("Autostart " + startElement['ObjectName'])
            self.createProcHandle(startElement)

    def getIdent(self):

        self.identGenMutex.lock()
        
        self.n_ident += 1 
        # check if current ident is already in use
        while list(filter(lambda item: item[0] == self.n_ident, self.processHandles.items())):
            self.n_ident += 1
        

        if not self.n_ident & 0x7fff:
            self.n_ident = 0
        self.identGenMutex.unlock()

        return self.n_ident

    def startExec(self, id, config):
        logging.debug('Operator::startExec() called - id: 0x{:08x}'.format(id))
        ## create processor and forward config and start filename

        self.currentConfig = config
        # https://stackoverflow.com/questions/34609935/passing-a-function-with-two-arguments-to-filter-in-python

        # return first element which matches the ID
        startElement = [x for x in config if x['Id'] == id][0]

        self.createProcHandle(startElement)

    def createProcHandle(self, element, inputData=None):    
        #logging.debug('Operator::startExec() called - id: 0x{:08x}'.format(id))

        self.procHandleMutex.lock()
        processHandles = self.processHandles.copy()
        self.procHandleMutex.unlock()

        procHandle = OperatorCreateProcHandle(element, inputData, processHandles, self)

        self.threadpool.start(procHandle)    

    def addHandle(self, identifier, handle):
        
        self.procHandleMutex.lock()
        self.processHandles[identifier] = handle
        self.procHandleMutex.unlock()

    def stopExec(self, id):
        logging.debug('Operator::stopExec() called - id: 0x{:08x}'.format(id))

        self.procHandleMutex.lock()
        processHandles = self.processHandles.copy()
        self.procHandleMutex.unlock()

        stopOperator = OperatorStopExec(processHandles, id, self)

        self.threadpool.start(stopOperator)

    def stopAll(self):

        logging.debug('Operator::stopAll() called')
        logging.info('User command: Stop All')
        self.procHandleMutex.lock()
        for threadIdentifier, processHandle in self.processHandles.items():
            processHandle.stop()
        self.procHandleMutex.unlock()

    def startAll(self, config):

        logging.info('User command: Start All')
        self.currentConfig = config
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
        processHandles = self.processHandles.copy()
        self.procHandleMutex.unlock()

        stateOperator = OperatorReturnElementState(processHandles, self)

        self.threadpool.start(stateOperator)
        
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

        self.command.emit(cmd)

    def highlightConnection(self, parentId, childId, wrkArea):

        logging.debug('Operator::updateStatus() called')
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

    def operationDone(self, id, area, record, identifier):

        logging.debug('Operator::operationDone() result received - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))

        if isinstance(record, GuiCMD):

            address = {
                'target'    : 'Element',  
                'id'        : id,
                'area'      : area            
            }
            cmd = { 
                'cmd'       : 'ElementText',
                'address'   : address,
                'data'      : record.text
            }
            self.command.emit(cmd)
            return
        
        operationDoneRunnable = OperatorElementOpDone(self.currentConfig, id, record, identifier, self)

        self.threadpool.start(operationDoneRunnable)
        
    def removeOperatorThread(self, id, identifier):
        
        logging.debug('Operator::removeOperatorThread() called - id: 0x{:08x}, ident: {:04d}'.format(id, identifier))

        self.procHandleMutex.lock()
        procHandle = self.processHandles[identifier]
        if procHandle.element["HighlightState"]:
            self.updateStatus(procHandle.element, False)

        del self.processHandles[identifier]

        self.procHandleMutex.unlock()