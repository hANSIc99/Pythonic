from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QCoreApplication as QC
from PyQt5.QtCore import QRunnable, QObject, QThreadPool
import multiprocessing as mp
import logging, sys, time, os, signal
from datetime import datetime
from Pythonic.record_function import Record, Function, alphabet

# additional declaration: already defined in elements/basicelements
class ExecRBFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):
        result = Record(self.getPos(), (self.row +1, self.column), record)
        return result

class ExecRFunction(Function):

    def __init__(self, config, b_debug, row, column):
        super().__init__(config, b_debug, row, column)

    def execute(self, record):
        result = Record(self.getPos(), (self.row, self.column+1), record)
        return result

class WorkerSignals(QObject):

    finished = pyqtSignal(object, name='element_finished' )
    pid_sig = pyqtSignal(object)

class GridOperator(QObject):

    update_logger   = pyqtSignal(name='update_logger')
    exec_pending    = pyqtSignal(name='exec_pending')
    switch_grid     = pyqtSignal('PyQt_PyObject', name='switch_grid')

    def __init__(self, grid, number):
        super().__init__()
        logging.debug('__init__() called on GridOperator')

        #grid: 3D-array [grid][row][col]
        # here is is only 2D: [row][col]
        #grid[0][row][column] = (function, config, self_sync)

        self.grid = grid
        self.number = number # grid number [0 .. 4]
        self.stop_flag = False
        self.fastpath = False # fastpath is active when debug is diasbled
        self.retry_counter = 0
        self.delay = 0
        self.threadpool = QThreadPool()
        self.b_debug_window = False
        self.pending_return = []
        self.pid_register = []
        self.exec_pending.connect(self.checkPending)
        logging.debug('__init__() GridOperator, threadCount: {}'.format(
            self.threadpool.maxThreadCount()))

    def startExec(self, start_pos, record=None):

        logging.debug('startExec() called, start_pos = {}'.format(start_pos))

        #function, config, self_sync = self.grid[start_pos[0]][start_pos[1]]
        function, self_sync = self.grid[start_pos[0]][start_pos[1]]
        logging.debug('GridOperator::startExec() function found: {}'.format(function))
        logging.debug('GridOperator::startExec() function dict: {}'.format(function.__dict__))
        logging.debug('GridOperator::startExec() config: {}'.format(function.config))


        self.update_logger.emit()
        executor = Executor(function, record, self.delay)
        executor.signals.finished.connect(self.execDone)
        executor.signals.pid_sig.connect(self.register_pid)
        self.threadpool.start(executor)

    def register_pid(self, pid):
        # register PID of spawned child process
        self.pid_register.append(pid)
        logging.debug('PID register: {}'.format(self.pid_register))

    def execDone(self, prg_return):

        logging.debug('execDone() called GridOperator from {}'.format(prg_return.source))

        logging.debug('PID returned: {}'.format(prg_return.pid))
        # remove returned pid from register
        try:
            self.pid_register.remove(prg_return.pid)
        except Exception as e:
            logging.error('De-registration of PID failed: {}'.format(e))


        # if an execption occured
        if(issubclass(prg_return.record_0.__class__, BaseException)):
            logging.error('Grid {} Target {}|{} Exception found: {}'.format(
                self.number + 1,
                prg_return.source[0],
                alphabet[prg_return.source[1]],
                prg_return.record_0))

            return

        ### proceed with regular execution ###

        # when the log checkbox is activated
        if prg_return.log:
            if prg_return.log_txt:
                logging.info('Grid {} Message {}|{} : {}'.format(
                            self.number + 1,
                            prg_return.source[0],
                            alphabet[prg_return.source[1]],
                            prg_return.log_txt))
            else:
                logging.info('Grid {} Message {}|{} : {}'.format(
                            self.number + 1,
                            prg_return.source[0],
                            alphabet[prg_return.source[1]],
                            prg_return.record_0))

        self.goNext(prg_return)

    def checkPending(self):

        logging.debug('GridOperator::checkPending() called')
        
        if self.pending_return:
            prg_return = self.pending_return.pop(0)
            self.execDone(prg_return)

    def proceedExec(self, prg_return):

        element = self.grid.itemAtPosition(*prg_return.source).widget()
        element.highlightStop()
        self.b_debug_window = False
        self.exec_pending.emit()
        self.goNext(prg_return)

    def goNext(self, prg_return):

        # check is target_0 includes a diffrent grid 
        # ExecReturn elemenot
        logging.debug('GridOperator::goNext() called, prg_return: {}'.format(prg_return))
        logging.debug('GridOperator::goNext() called, target_0: {}'.format(prg_return.target_0))

        if prg_return.target_0:
            logging.debug('GridOperator::goNext() called with next target_0: {}'.format(prg_return.target_0))
            logging.debug('GridOperator::goNext() called with record_0: {}'.format(prg_return.record_0))

            if len(prg_return.target_0) == 3: # switch grid, go over main
                # fastpath = True
                self.switch_grid.emit(prg_return)
                return
                
            #Proceed as usual
            new_rec = self.fastPath(prg_return.target_0, prg_return.record_0)
            if new_rec: # check for ExecR or ExecRB
                self.goNext(new_rec)
            else: # if nothing found: proceed as usual
                self.startExec(prg_return.target_0, prg_return.record_0)

        if prg_return.target_1:

            logging.debug('GridOperator::goNext() called with additional target_1: {}'.format(
                prg_return.target_1))
            logging.debug('GridOperator::goNext() called with record_1: {}'.format(prg_return.record_1))

            # self_sync is true on basic_sched and binancesched
            #self_sync = self.grid.itemAtPosition(*prg_return.target_1).widget().self_sync
            #function, config, self_sync = self.grid[prg_return.target_1[0]][prg_return.target_1[1]] 
            function, self_sync = self.grid[prg_return.target_1[0]][prg_return.target_1[1]] 

            if not self_sync:
                new_rec = self.fastPath(prg_return.target_1, prg_return.record_1)
                logging.debug('GridOperator::goNext() exception here')
                logging.debug('GridOperator::goNext() new_rec: {}'.format(new_rec))
                self.goNext(new_rec)
            else:
                self.startExec(prg_return.target_1, prg_return.record_1)

    def fastPath(self, target_0, record):
        row, col = target_0
        logging.debug('GridOperator::fastPath() check row: {} col: {}'.format(*target_0))
        #element = self.grid.itemAtPosition(*target).widget()
        #[row][column] = (function, config, self_sync)
        #function, config, self_sync = self.grid[row][col] 
        function, self_sync = self.grid[row][col] 
        logging.debug('GridOperator::fastPath() function: {}'.format(function))
        logging.debug('GridOperator::fastPath() isinstance ExecRB: {}'.format(isinstance(function, ExecRBFunction)))
        logging.debug('GridOperator::fastPath() isinstance ExecRB#####: {} '.format(str(type(function))))
        logging.debug('GridOperator::fastPath() isinstance ExecR: {}'.format(isinstance(function, ExecRFunction)))

        if str(type(function)) == "<class 'Pythonic.elements.basicelements_func.ExecRBFunction'>": # jump to the next target
            # record_1 -> record_0 when goNext() is called recursively
            # returning only target_0 and record_0
            new_rec = Record((row, col-1), (row+1, col), record)
            return new_rec
        elif str(type(function)) == "<class 'Pythonic.elements.basicelements_func.ExecRFunction'>": # jump to the next target
            #hier testen ob target fings
            # record_1 -> record_0 when goNext() is called recursively
            # returning only target_0 and record_0
            new_rec = Record((row, col-1), (row, col+1), record)
            return new_rec
        else:
            return None

            
    def highlightStop(self, position):
        logging.debug('highlightStop() called for position {}'.format(position))
        element = self.grid.itemAtPosition(*position).widget()
        element.highlightStop()

    def stop_execution(self):
        logging.debug('stop_execution() called')
        self.stop_flag = True

    def kill_proc(self):
        logging.debug('kill_proc() called')

        for proc in self.pid_register:
            try:
                os.kill(proc, signal.SIGTERM)
                logging.info('Process killed, PID {}'.format(proc))
            except Exception as e:
                pass

        self.pid_register.clear()


class Executor(QRunnable):


    def __init__(self, function, record, delay):
        super().__init__()
        #BAUSTELLE: element = function
        logging.debug('Executor::__init__() called')
        self.function = function
        self.record = record
        #self.stop_flag = False
        self.retry_counter = 0
        self.delay = delay
        self.signals = WorkerSignals()

    def run(self):

        logging.debug('Executor::run() called -  pid: {} at {}'.format(os.getpid(), datetime.now()))

        self.start_proc(self.function, self.record, self.delay, 1)

        logging.debug('Executor::run() returned - pid: {} returned at {}'.format(os.getpid(), datetime.now()))


    def start_proc(self, function, record, delay, retries):
        # Bug: Sometimes the Exception windows isnt triggered
        logging.debug('Executor::start_proc() called with programm: {}'.format(function))
            
        return_pipe_0, feed_pipe_0 = mp.Pipe(duplex=False)

        p_0 = mp.Process(target=target_0, args=(function, record, feed_pipe_0, ))

        p_0.start()
        self.signals.pid_sig.emit(p_0.pid) 
        time.sleep(delay)
        
        result = return_pipe_0.recv()
        p_0.join()

        self.signals.finished.emit(result)

def target_0(function, record, feed_pipe):

    ret = function.execute_ex(record)
    feed_pipe.send(ret)
