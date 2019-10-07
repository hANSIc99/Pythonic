import sys, signal, logging, pickle, datetime, os
import multiprocessing as mp
from pathlib import Path
from workingarea               import WorkingArea
from PyQt5.QtCore import QCoreApplication, QObject, QTimer, QThreadPool
#workingarea import
from PyQt5.QtWidgets import QWidgetItem, QFrame, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from executor_daemon import GridOperator

"""
from Pythonic.elements.basicelements     import StartElement, ExecRB, ExecR, PlaceHolder
from Pythonic.elements.basic_operation   import ExecOp
from Pythonic.elements.basic_branch      import ExecBranch
from Pythonic.elements.basic_return      import ExecReturn
from Pythonic.elements.basic_process     import ExecProcess
from Pythonic.elements.basic_ta          import ExecTA
from Pythonic.elements.basic_sched       import ExecSched
from Pythonic.elements.basic_stack       import ExecStack
from Pythonic.elements.binance_sched     import BinanceSched
from Pythonic.elements.binance_ohlc      import BinanceOHLC
from Pythonic.elements.binance_order     import BinanceOrder
from Pythonic.elements.conn_mail         import ConnMail
from Pythonic.elements.conn_rest         import ConnREST
from Pythonic.elements.ml_svm            import MLSVM
from Pythonic.elements.ml_svm_predict    import MLSVM_Predict

from Pythonic.executor                   import GridOperator
from Pythonic.elementmaster              import ElementMaster
from Pythonic.dropbox                    import DropBox
"""


class MainWorker(QObject):

    log_level = logging.DEBUG
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')

    max_grid_size = 50

    def __init__(self, app):
        super(MainWorker, self).__init__()
        self.app = app
        self.threadpool = QThreadPool()
        mp.set_start_method('spawn')

        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)
        self.log_date = datetime.datetime.now()

        log_date_str = self.log_date.strftime('%Y_%m_%d')
        month = self.log_date.strftime('%b')
        year = self.log_date.strftime('%Y')
        home_dict = str(Path.home())
        file_path = '{}/PythonicDaemon_{}/{}/log_{}.txt'.format(home_dict, year, month, log_date_str) 
        self.ensure_file_path(file_path)

        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self.formatter)

        self.logger.addHandler(file_handler)


        logging.debug('MainWorker::__init__() called')

    def ensure_file_path(self, file_path):

        directory = os.path.dirname(file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

    def update_logfile(self):

        now = datetime.datetime.now().date()
        if (now != self.log_date.date()):
            self.logger.removeHandler(self.logger.handlers[0])
            log_date_str = now.strftime('%Y_%m_%d')
            month = now.strftime('%b')
            year = now.strftime('%Y')
            home_dict = str(Path.home())
            file_path = '{}/PythonicDaemon_{}/{}/log_{}.txt'.format(home_dict, year, month, log_date_str) 
            self.ensure_file_path(file_path)
            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
            self.log_date = datetime.datetime.now()

    def start(self, args):
        grid_files = []
        self.checkArgs(args[1:], grid_files)

        logging.debug('MainWorker::start() called')
        logging.debug('MainWorker::start() Open the following files: {}'.format(grid_files))

        self.loadGrid(grid_files[0])

        #self.wrk_area = (QObject)WorkingArea()

    def loadGrid(self, filename):

        #logging.debug('WorkingArea::loadGrid() called with filename {}'.format(filename))
        logging.debug('MainWorker::loadGrid() called with filename {}'.format(filename))

        try:
            f = open(filename, 'rb')
            try:
                element_list = pickle.load(f)
                #self.clearGrid()
            except Exception as e:
                #logging.error('loadGrid() pickle cant be loaded: {}'.format(e))
                print('loadGrid() pickle cant be loaded: {}'.format(e))

            finally:
                f.close()
        except Exception as e:
            #logging.error('loadGrid() file cant be read: {}'.format(e))
            print('loadGrid() file cant be read: {}'.format(e))

            return

        #5 grid [row, column]
        grid = [[[None for k in range(self.max_grid_size)]for i in range(self.max_grid_size)]for j in range(5)]
        
        # populate the grid
        for element in element_list:
            
                # Element description: (pos, function, config, log,  self_sync)
                
                pos, function, config, self_sync = element
                row, column = pos
                logging.debug('MainWorker::loadGrid() row: {} col: {}'.format(row, column))
                grid[0][row][column] = (function, config, self_sync)

        self.grid_operator = GridOperator(grid[0])
        # __init__(self, config, row, column):
        # pos = (row, column)
        # return.log_txt return.log
        self.grid_operator.startExec((0,0))
        
        function.__init__(config, True, *pos)
        result = function.execute('test 123')
        print(result.source)
        print(result.target_0)
        print(result.log_txt)
        print(result.record_0)

        """
        # second run: add child and parent relation
        for element in element_list:
            row, col = element.getPos()
                
            if element.child_pos[0]:

                child = self.grid.itemAtPosition(row+1, col).widget()
                element.setChild(child)

            if element.child_pos[1]:

                child = self.grid.itemAtPosition(row, col+1).widget()
                element.setChild(child)
            

            if (type(element).__name__ == ExecR.__name__ or
                type(element).__name__ == ExecRB.__name__):
                parent = self.grid.itemAtPosition(row, col-1)
                logging.debug('WorkingArea::loadGrid() parent:{}'.format(
                    parent))

                logging.debug('WorkingArea::loadGrid() type parent:{}'.format(
                    type(parent)))


                parent = self.grid.itemAtPosition(row, col-1).widget()
                element.parent_element = parent
            #elif not isinstance(element, StartElement):

            elif (type(element).__name__ != StartElement.__name__):
                parent = self.grid.itemAtPosition(row-1, col).widget()
                element.parent_element = parent

            #if isinstance(element, PlaceHolder):

            if (type(element).__name__ == PlaceHolder.__name__):    
                element.func_drop.connect(self.addElement)
                #element.query_config.connect(self.loadConfig)
            else:
                element.del_sig.connect(self.delete_element)
        """


    def checkArgs(self, args, grid_files):
        for argument in args:
            if argument[0] == '-' or argument[0] == '--':
                print('Option found: {}'.format(argument))
            else:
                print('Filename found: {}'.format(argument))
                grid_files.append(argument)




if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *argc: QCoreApplication.quit())
    print('##################Start################')
    grid_files = []
    app = QCoreApplication(sys.argv)
    print('argc: {}'.format(app.arguments()))
    print('app-name: {}'.format(app.applicationName()))

    timer = QTimer()
    timer.timeout.connect(lambda *args: None) # cathing signals outside the QT eventloop (e.g. SIGINT)
    timer.start(100)

    ex = MainWorker(app)
    ex.start(sys.argv)

    app.exec_()
