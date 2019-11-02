import sys, signal, logging, pickle, datetime, os, time
import multiprocessing as mp
from pathlib import Path
from Pythonic.workingarea               import WorkingArea
from PyQt5.QtCore import QCoreApplication, QObject, QTimer, QThread
#workingarea import
from PyQt5.QtWidgets import QWidgetItem, QFrame, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from Pythonic.executor_daemon import GridOperator

class stdinReader(QThread):

    kill_all    = pyqtSignal(name='kill_all')
    print_procs = pyqtSignal(name='print_procs')
    def run(self):
        while True:
            cmd = sys.stdin.read(1) # reads one byte at a time
            if cmd == ('q' or 'Q'):
                print('Stopping all processes....')
                self.kill_all.emit()
                time.sleep(3) # wait for 3 seconds to kill all processes
                QCoreApplication.quit()
            elif cmd == ('s' or 'S'):
                self.print_procs.emit()


class MainWorker(QObject):

    log_level = logging.INFO
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')

    max_grid_size = 50
    max_grid_cnt  = 5
    
    welcome_msg =   ' ____        _   _                 _      ____                                   \n'\
                    '|  _ \ _   _| |_| |__   ___  _ __ (_) ___|  _ \  __ _  ___ _ __ ___   ___  _ __  \n'\
                    '| |_) | | | | __| \'_ \ / _ \| \'_ \| |/ __| | | |/ _` |/ _ \ \'_ ` _ \ / _ \| \'_ \ \n'\
                    '|  __/| |_| | |_| | | | (_) | | | | | (__| |_| | (_| |  __/ | | | | | (_) | | | |\n'\
                    '|_|    \__, |\__|_| |_|\___/|_| |_|_|\___|____/ \__,_|\___|_| |_| |_|\___/|_| |_|\n'\
                    '|___/                                                                     \n\n'

    log_info_msg    = '<<<<<<<<<<<< Logging directory ~/PythonicDaemon_201x/Month/\n'
    input_info_msg  = '>>>>>>>>>>>> Enter \'q\' to stop execution'
    status_info_msg = '>>>>>>>>>>>> Enter \'s\' to list all background processes\n'

    def __init__(self, app):
        super(MainWorker, self).__init__()
        self.app = app
        mp.set_start_method('spawn')
        self.stdinReader = stdinReader()
        self.stdinReader.print_procs.connect(self.printProcessList)
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

    def printProcessList(self):
        for i in range(self.active_grids):
            if self.grd_ops_arr[i].pid_register:
                for pid in self.grd_ops_arr[i].pid_register:
                    print('>> Grid {} - PID: {}'.format(str(i+1), str(pid)))
        print('\n')

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
        print('\n Arguments: {}'.format(args[2:]))
        print(self.welcome_msg)

        # first argument is main_console.py
        # second argument is script location
        if not args[2:]:
            print('No files specified - nothing to do')
            sys.exit()

        self.checkArgs(args[2:], grid_files)

        logging.debug('MainWorker::start() called')
        logging.debug('MainWorker::start() Open the following files: {}'.format(grid_files))

        print(self.log_info_msg)
        print(self.input_info_msg)
        print(self.status_info_msg)
        self.loadGrid(grid_files)
        self.stdinReader.start()

            
        
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
            self.grd_ops_arr[i].switch_grid.connect(self.receiveTarget)
            self.stdinReader.kill_all.connect(self.grd_ops_arr[i].kill_proc)
            self.grd_ops_arr[i].startExec((0,0))
            #count number of active grids
            self.active_grids = i+1

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
