from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QRunnable, QObject, QThreadPool
import multiprocessing as mp
import logging, sys, time, traceback, os, signal
from datetime import datetime

from Pythonic.record_function import Record, PipeRecord
from Pythonic.elementeditor import ElementEditor
from Pythonic.record_function import alphabet
from Pythonic.exceptwindow import ExceptWindow
from Pythonic.debugwindow import DebugWindow
from Pythonic.elements.basic_stack import ExecStack
from Pythonic.elements.basic_sched import ExecSched
from Pythonic.elements.basicelements import ExecRB, ExecR

# uncomment this during development
"""
from record_function import Record, PipeRecord
from elementeditor import ElementEditor
from record_function import alphabet
from exceptwindow import ExceptWindow
from debugwindow import DebugWindow
from elements.basic_stack import ExecStack
from elements.basic_sched import ExecSched
from elements.basicelements import ExecRB, ExecR
"""
class WorkerSignals(QObject):

    finished = pyqtSignal(object, name='element_finished' )
    ret_pipe = pyqtSignal(object, name='pipe_data')
    pid_sig = pyqtSignal(object)

class GridOperator(QObject):

    update_logger   = pyqtSignal(name='update_logger')
    exec_pending    = pyqtSignal(name='exec_pending')
    switch_grid     = pyqtSignal('PyQt_PyObject', name='switch_grid')

    def __init__(self, grid, number):
        super().__init__()
        logging.debug('__init__() called on GridOperator')
        self.grid = grid
        self.number = number # number of workingarea [0-4]
        self.stop_flag = False # indicates if normale execution is stopped
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

        try:
            element = self.grid.itemAtPosition(*start_pos).widget()
        except AttributeError as e:
            return

        if self.stop_flag:
            return
        self.update_logger.emit()
        executor = Executor(element, record, self.delay)
        executor.signals.finished.connect(self.execDone)
        executor.signals.ret_pipe.connect(self.execDone)
        executor.signals.pid_sig.connect(self.register_pid)
        element.highlightStart()
        self.threadpool.start(executor)

    def register_pid(self, pid):
        # register PID of spawned child process
        self.pid_register.append(pid)
        logging.debug('PID register: {}'.format(self.pid_register))


    def execDone(self, prg_return):

        logging.debug('execDone() called GridOperator from {}'.format(prg_return.source))

        element = self.grid.itemAtPosition(*prg_return.source).widget()

        logging.debug('PID returned: {}'.format(prg_return.pid))
        # remove returned pid from register if prg_return is not coming from pipe
        if not type(prg_return).__name__ == PipeRecord.__name__:
            try:
                # does not work in case of an exception
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

                element.highlightException()
                self.exceptwindow = ExceptWindow(str(prg_return.record_0), prg_return.source)
                self.exceptwindow.window_closed.connect(self.highlightStop)
                return

        ### proceed with regular execution ###

        # when the log checkbox is activated
        if prg_return.log:
            if prg_return.log_txt:
                logging.info('Grid: {} Message {}|{} : {}'.format(
                            self.number + 1,
                            prg_return.source[0],
                            alphabet[prg_return.source[1]],
                            prg_return.log_txt))
            else:
                logging.info('Grid: {} Message {}|{} : {}'.format(
                            self.number + 1,
                            prg_return.source[0],
                            alphabet[prg_return.source[1]],
                            prg_return.record_0))



        # when the debug button on the element is active
        if element.b_debug:

            logging.debug('GridOperator::execDone() b_debug_window = {}'.format(self.b_debug_window))

            if isinstance(element, ExecStack): # don't open the regular debug window

                logging.debug('GridOperator::execDone()Special window for Exec stack element')
                element.highlightStop()
                self.goNext(prg_return)

            # check if there is already an open debug window
            elif not self.b_debug_window:

                self.debugWindow = DebugWindow(str(prg_return.record_0), prg_return.source)
                self.debugWindow.proceed_execution.connect(lambda: self.proceedExec(prg_return))
                self.debugWindow.raiseWindow() # open debug window

                #if not element.self_sync:
                self.b_debug_window = True

            
            else:
                #queue element
                self.pending_return.append(prg_return)

        else:
            # highlight stop only when element return
            if not type(prg_return).__name__ == PipeRecord.__name__:
                element.highlightStop() 

            self.goNext(prg_return)

    def checkPending(self):

        logging.debug('GridOperator::checkPending() called')
        
        if self.pending_return:
            prg_return = self.pending_return.pop(0)
            self.execDone(prg_return)

    def proceedExec(self, prg_return):

        element = self.grid.itemAtPosition(*prg_return.source).widget()
        if not type(prg_return).__name__ == PipeRecord.__name__:
            element.highlightStop()
        self.b_debug_window = False
        self.exec_pending.emit()
        self.goNext(prg_return)

    def goNext(self, prg_return):

        # check is target_0 includes a diffrent grid 
        # ExecReturn elemenot

        if prg_return.target_0:
            logging.debug('GridOperator::goNext() called with next target_0: {}'.format(prg_return.target_0))
            logging.debug('GridOperator::goNext() called with record_0: {}'.format(prg_return.record_0))

            if self.fastpath:

                if len(prg_return.target_0) == 3: # switch grid, go over main
                    # fastpath = True
                    self.switch_grid.emit((prg_return, True))
                    return
                
                new_rec = self.fastPath(prg_return.target_0, prg_return.record_0)
                if new_rec: # check for ExecR or ExecRB
                    self.goNext(new_rec)
                else: # if nothing found: proceed as usual
                    self.startExec(prg_return.target_0, prg_return.record_0)
            else:

                if len(prg_return.target_0) == 3: # switch grid, go over main
                    # fastpath = False
                    self.switch_grid.emit((prg_return, False))
                    return

                self.startExec(prg_return.target_0, prg_return.record_0)

        if prg_return.target_1:

            logging.debug('GridOperator::goNext() called with additional target_1: {}'.format(
                prg_return.target_1))
            logging.debug('GridOperator::goNext() called with record_1: {}'.format(prg_return.record_1))

            # self_sync is true on basic_sched and binancesched
            self_sync = self.grid.itemAtPosition(*prg_return.target_1).widget().self_sync

            if self.fastpath and not self_sync:
                new_rec = self.fastPath(prg_return.target_1, prg_return.record_1)
                logging.debug('GridOperator::goNext() execption here')
                logging.debug('GridOperator::goNext() new_rec: {}'.format(new_rec))
                self.goNext(new_rec)
            else:
                self.startExec(prg_return.target_1, prg_return.record_1)

    def fastPath(self, target, record):

        logging.debug('GridOperator::fastPath() check row: {} col: {}'.format(*target))
        element = self.grid.itemAtPosition(*target).widget()

        if isinstance(element, ExecRB): # jump to the next target
            # record_1 -> record_0 when goNext() is called recursively
            # returning only target_0 and record_0
            new_rec = Record(element.getPos(), (element.row+1, element.column), record)
            return new_rec
        elif isinstance(element, ExecR): # jump to the next target
            #hier testen ob target fings
            # record_1 -> record_0 when goNext() is called recursively
            # returning only target_0 and record_0
            new_rec = Record(element.getPos(), (element.row, element.column+1), record)
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
            os.kill(proc, signal.SIGTERM)
            logging.info('Process killed, PID {}'.format(proc))

        self.pid_register.clear()


class Executor(QRunnable):


    def __init__(self, element, record, delay):
        super().__init__()
        logging.debug('Executor::__init__() called')
        self.element = element
        self.record = record
        self.stop_flag = False
        self.retry_counter = 0
        self.delay = delay
        self.signals = WorkerSignals()

    def run(self):

        logging.debug('Executor::run() called with target {} pid {} at {}'.format(
            self.element.getPos(), os.getpid(), datetime.now()))

        self.start_proc(self.element.function, self.record, self.delay, 1)

        logging.debug('Executor::run() returned from {}, pid: {} returned at {}'.format(
            self.element.getPos(), os.getpid(), datetime.now()))


    def start_proc(self, function, record, delay, retries):
        # Bug: Sometimes the Exception windows isnt triggered
        logging.debug('Executor::start_proc() called with programm: {}'.format(function))
            
        return_pipe_0, feed_pipe_0 = mp.Pipe(duplex=False)

        p_0 = mp.Process(target=target_0, args=(function, record, feed_pipe_0, ))

        p_0.start()
        self.signals.pid_sig.emit(p_0.pid) 
        time.sleep(delay)
        result = return_pipe_0.recv()
        while type(result).__name__ != Record.__name__:
            #logging.info('Passt!: {}'.format(result.record_0))
            if type(result).__name__ == PipeRecord.__name__:
                self.signals.ret_pipe.emit(result)

            result = return_pipe_0.recv()

        p_0.join()

        self.signals.finished.emit(result)

def target_0(function, record, feed_pipe):

    def callback(feed_data): feed_pipe.send(feed_data)
    ret = function.execute_ex(record, callback)
    feed_pipe.send(ret)
