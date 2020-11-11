import sys, logging, pickle, datetime, os, signal, time, itertools, tty, termios, select
import multiprocessing as mp
from threading import Timer, Thread, Event
from pathlib import Path
from zipfile import ZipFile
from PyQt5.QtCore import QCoreApplication, QObject, QThread, Qt, QTimer
from PyQt5.QtCore import pyqtSignal

from Pythonic.executor_daemon import GridOperator

def reset_screen():

    welcome_msg =   ' ____        _   _                 _      ____                                   \n'\
                    '|  _ \ _   _| |_| |__   ___  _ __ (_) ___|  _ \  __ _  ___ _ __ ___   ___  _ __  \n'\
                    '| |_) | | | | __| \'_ \ / _ \| \'_ \| |/ __| | | |/ _` |/ _ \ \'_ ` _ \ / _ \| \'_ \ \n'\
                    '|  __/| |_| | |_| | | | (_) | | | | | (__| |_| | (_| |  __/ | | | | | (_) | | | |\n'\
                    '|_|    \__, |\__|_| |_|\___/|_| |_|_|\___|____/ \__,_|\___|_| |_| |_|\___/|_| |_|\n'\
                    '       |___/                                                                     \n'

    version         = 'v0.18\n'
    gitHub          = 'Visit https://github.com/hANSIc99/Pythonic\n'
    log_info_msg    = '<<<<<<<<<<<< Logging directory ~/PythonicDaemon_201x/Month/\n'
    input_info_msg  = '>>>>>>>>>>>> Enter \'q\' to stop execution'
    status_info_msg = '>>>>>>>>>>>> Hold  \'p\' to list all background processes'
    applog_info_msg = '>>>>>>>>>>>> Enter \'l\' to show log messages\n'

    os.system('clear')

    print('\n')
    print(welcome_msg)
    print(version)
    print(gitHub)
    print(log_info_msg)
    print(input_info_msg)
    print(status_info_msg)
    print(applog_info_msg)

class stdinReader(QThread):

    print_procs = pyqtSignal(name='print_procs')
    quit_app = pyqtSignal(name='quit_app')
    finished = pyqtSignal(name='finished')
    b_init      = True
    b_exit      = False
    b_log       = False
    b_procs     = False
    interval    = 0.5
    max_log_lines = 20
    spinner = itertools.cycle(['-', '\\', '|', '/'])

    def __init__(self):
        super().__init__()
        self.startTime = time.time()

    def run(self):

        if self.b_init:
            self.b_init = False
            self.fd = sys.stdin.fileno() 
            if os.isatty(sys.stdin.fileno()):
                self.old_settings = termios.tcgetattr(self.fd) 
                tty.setraw(sys.stdin.fileno()) 

        while not self.b_exit:

            rd_fs, wrt_fs, err_fs =  select.select([sys.stdin], [], [], self.interval)

            if rd_fs and os.isatty(sys.stdin.fileno()):
                cmd = rd_fs[0].read(1)

                if cmd == ('q' or 'Q'): # quit
                    termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
                    termios.tcflush(self.fd, termios.TCIOFLUSH)
                    self.b_exit = True
                    self.quit_app.emit()

                elif cmd == ('p' or 'P'): # show proccesses
                    self.b_procs = True
                    termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
                    self.print_procs.emit()
                    tty.setraw(sys.stdin.fileno()) 

                elif cmd == ('l' or 'L'): # show log
                    if self.b_log:
                        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
                        reset_screen() # reset the screen to hide the log list
                        tty.setraw(sys.stdin.fileno()) 
                    self.b_log = not self.b_log
                    
                else:
                    sys.stdout.write('\b')

            else:
                if os.isatty(sys.stdin.fileno()):
                    self.callback()



    def callback(self):

        if self.b_procs:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            reset_screen() # reset the screen to hide the log list
            tty.setraw(sys.stdin.fileno()) 

        if self.b_log:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            reset_screen()
            print('Log output active:\n')
            self.tail(self.max_log_lines)
            tty.setraw(sys.stdin.fileno()) 

        uptime  = time.time() - self.startTime
        minutes = int(uptime // 60 % 60)
        hours   = int(uptime // 3600 % 24)
        days    = int(uptime // 86400)

        sys.stdout.write('Running... ' + next(self.spinner) + 
        '                                           ' +
         'Uptime: {:02d}:{:02d} - {:03d} days'.format(hours, minutes, days))

        sys.stdout.flush()
        sys.stdout.write('\r')

    def tail(self, lines):

        now = datetime.datetime.now().date()
        month = now.strftime('%b')
        year = now.strftime('%Y')
        home_dict = str(Path.home())
        file_path = '{}/PythonicDaemon_{}/{}/log_{}.txt'.format(home_dict, year, month, self.log_date_str) 

        BLOCK_SIZE = 1024


        with open(file_path, 'rb') as f:
            f.seek(0, 2) # set fp to 0 from end of file
            block_end_byte = f.tell() # tell() returns the current fp position
            block_number = -1
            blocks = []
            lines_to_go = lines

            while lines_to_go > 0 and block_end_byte > 0:
                if (block_end_byte - BLOCK_SIZE > 0): # bytes to read > BLOCK_SIZE
                    f.seek(block_number * BLOCK_SIZE, 2) # set fp 1 block backwards
                    blocks.append(f.read(BLOCK_SIZE))
                else:
                    f.seek(0,0) # set fp to the beginning
                    blocks.append(f.read(block_end_byte)) # read the rest

                lines_found = blocks[-1].count(b'\n') # count occurences of \n
                lines_to_go -= lines_found
                block_end_byte -= BLOCK_SIZE # move local pointer backwards
                block_number -= 1

            log_display_txt = b''.join(reversed(blocks))
            log_display_txt = b'\n'.join(log_display_txt.splitlines()[-lines:])
            log_display_txt = log_display_txt.decode('utf-8')

            print(log_display_txt + '\n')

    def updateLogDate(self, log_date_str):
        logging.debug('stdinReader::updateLogDate() called with: {}'.format(log_date_str))
        self.log_date_str = log_date_str


class MainWorker(QObject):

    kill_all        = pyqtSignal(name='kill_all')
    update_logdate  = pyqtSignal('PyQt_PyObject', name='update_logdate')
    log_level       = logging.INFO
    formatter       = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')


    max_grid_size = 50
    max_grid_cnt  = 5
    

    def __init__(self, app):
        super(MainWorker, self).__init__()
        self.app = app
        mp.set_start_method('spawn')
        self.stdinReader = stdinReader()
        self.stdinReader.print_procs.connect(self.printProcessList)
        self.stdinReader.quit_app.connect(self.exitApp)
        self.update_logdate.connect(self.stdinReader.updateLogDate)
        self.grd_ops_arr    = []
        self.fd = sys.stdin.fileno()
        if os.isatty(sys.stdin.fileno()):
            self.orig_tty_settings = termios.tcgetattr(self.fd) 

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
        self.update_logdate.emit(log_date_str) # forward log_date_str to instance of stdinReader


        logging.debug('MainWorker::__init__() called')

    def exitApp(self):
        print('# Stopping all processes....')
        self.kill_all.emit()
        time.sleep(3) # wait for 1 seconds to kill all processes
        self.app.quit()
        os.kill(self.app.applicationPid(), signal.SIGTERM) # kill all related threads


    def ensure_file_path(self, file_path):

        directory = os.path.dirname(file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

    def printProcessList(self):
        b_proc_found = False
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.orig_tty_settings)
        reset_screen()
        for i in range(self.max_grid_cnt):
            if self.grd_ops_arr[i].pid_register:
                for pid in self.grd_ops_arr[i].pid_register:
                    b_proc_found = True
                    print('# Grid {} - PID: {}'.format(str(i+1), str(pid)))
        if not b_proc_found:
            print('# Currently no processes running')

        print('\n')
        tty.setraw(sys.stdin.fileno()) 

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
            self.update_logdate.emit(log_date_str)

    def start(self, args):

        #print('\n Arguments: {}'.format(args))
        reset_screen()        
        # first argument is main_console.py
        # second argument is script location

        grid_file = self.checkArgs(args[1:])

        if not grid_file:
            print('No file specified - nothing to do')
            sys.exit()


        logging.debug('MainWorker::start() called')
        logging.debug('MainWorker::start() Open the following file: {}'.format(grid_file))

        self.loadGrid(grid_file)

        self.stdinReader.start() # call run() method in separate thread

        """
        b_finished = False         

        while not b_finished: # when thread return, exit application
            time.sleep(1)
            b_finished = self.stdinReader.isFinished()
 
        logging.info('MainWorker::Returning from thread')
        self.kill_all.emit()
        """

    def on_callback(self):

        self.stdinReader.run()


    def loadGrid(self, filename):

        logging.debug('MainWindow::loadGrid() called')

        grid = [[[None for k in range(self.max_grid_size)]for i in range(self.max_grid_size)]
                for j in range(self.max_grid_cnt)]

        with ZipFile(filename, 'r') as archive:
            for i, zipped_grid in enumerate(archive.namelist()):
                pickled_grid = archive.read(zipped_grid)
                element_list = pickle.loads(pickled_grid)
                # first char repesents the grid number
                for element in element_list:
                    # Element description: (pos, function, config, log,  self_sync)
                    pos, element_type, function, config, self_sync = element
                    row, column = pos
                    logging.debug('MainWorker::loadGrid() row: {} col: {}'.format(row, column))
                    grid[i][row][column] = (function, self_sync)

                self.grd_ops_arr.append(GridOperator(grid[i], i))
                self.grd_ops_arr[i].switch_grid.connect(self.receiveTarget)
                self.grd_ops_arr[i].update_logger.connect(self.update_logfile)
                self.kill_all.connect(self.grd_ops_arr[i].kill_proc)
                self.grd_ops_arr[i].startExec((0,0))


        archive.close()
           
        
    def receiveTarget(self, prg_return):

        grid, *pos = prg_return.target_0
        logging.debug('MainWorker::receiveTarget() called from pos: {} goto grid: {}'.format(pos, grid))
        # go to goNext() in the target grid
        # set fastpath variable

        # remove grid from target_0 
        prg_return.target_0 = pos
        self.grd_ops_arr[grid].goNext(prg_return)


    def checkArgs(self, args):

        b_file_found = False
        grid_file = None

        for argument in args:
            if argument[0] == '-' or argument[0] == '--':
                print('Option found: {}'.format(argument))
            else:
                if not b_file_found:
                    b_file_found = True
                    grid_file = argument

        return grid_file
