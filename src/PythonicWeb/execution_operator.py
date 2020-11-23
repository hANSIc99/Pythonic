import sys, logging, pickle, datetime, os, signal, time, itertools, tty, termios, select
from PyQt5.QtCore import QCoreApplication, QObject, QThread, Qt, QTimer
from PyQt5.QtCore import pyqtSignal



class Operator(QThread):

    def __init__(self,):
        super().__init__()

    def run(self):

        while True:
            time.sleep(1)
            #logging.debug('Operator::run() called')

    def startExec(self, id):
        logging.debug('Operator::startExec() called - id: {:08x}'.format(id))