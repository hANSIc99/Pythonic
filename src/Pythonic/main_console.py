import sys, signal, logging, pickle, datetime, os
import multiprocessing as mp
from pathlib import Path
from workingarea               import WorkingArea
from PyQt5.QtCore import QCoreApplication, QObject, QTimer, QThreadPool
#workingarea import
from PyQt5.QtWidgets import QWidgetItem, QFrame, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from executor_daemon import GridOperator

class MainWorker(QObject):

    log_level = logging.INFO
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')

    max_grid_size = 50
    max_grid_cnt  = 5

    def __init__(self, app):
        super(MainWorker, self).__init__()
        self.app = app
        self.threadpool = QThreadPool()
        mp.set_start_method('spawn')
        self.grd_ops_arr    = []

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

        self.loadGrid(grid_files)

    def loadGrid(self, grid_files):

        #5 grid [row, column]
        grid = [[[None for k in range(self.max_grid_size)]for i in range(self.max_grid_size)]
                for j in range(self.max_grid_cnt)]

        for i, filename in enumerate(grid_files):
            logging.debug('MainWorker::loadGrid() called with filename {}'.format(filename))
            if i >= self.max_grid_cnt:
                print('Maximum number if grids reached, file \'{}\' won\'t be loaded'.format(
                    filename))
                return


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

            print('Load file - Grid: {} file: \'{}\' found'.format(i+1, filename))
            # populate the grid
            for element in element_list:
            
                # Element description: (pos, function, config, log,  self_sync)
                pos, function, config, self_sync = element
                row, column = pos
                logging.debug('MainWorker::loadGrid() row: {} col: {}'.format(row, column))
                #grid[0][row][column] = (function, config, self_sync)
                grid[i][row][column] = (function, self_sync)

            self.grd_ops_arr.append(GridOperator(grid[i]))
            self.grd_ops_arr[i].startExec((0,0))
            self.grd_ops_arr[i].switch_grid.connect(self.receiveTarget)

    def receiveTarget(self, prg_return):

        grid, *pos = prg_return.target_0
        logging.debug('MainWorker::receiveTarget() called from pos: {} goto grid: {}'.format(pos, grid))
        # go to goNext() in the target grid
        # set fastpath variable

        # remove grid from target_0 
        prg_return.target_0 = pos
        self.grd_ops_arr[grid].goNext(prg_return)


    def checkArgs(self, args, grid_files):
        for argument in args:
            if argument[0] == '-' or argument[0] == '--':
                print('Option found: {}'.format(argument))
            else:
                grid_files.append(argument)



if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *argc: QCoreApplication.quit())
    grid_files = []
    app = QCoreApplication(sys.argv)

    timer = QTimer()
    timer.timeout.connect(lambda *args: None) # cathing signals outside the QT eventloop (e.g. SIGINT)
    timer.start(100)

    ex = MainWorker(app)
    ex.start(sys.argv)

    app.exec_()
