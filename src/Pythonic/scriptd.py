#!/usr/local/bin/python3

import os, sys, Pythonic
from subprocess import Popen, PIPE

import sys, signal, logging, pickle, datetime, os, time
import multiprocessing as mp
from pathlib import Path
from zipfile import ZipFile
from Pythonic.workingarea               import WorkingArea
from Pythonic.main_daemon import MainWorker
from PyQt5.QtCore import QCoreApplication, QObject, QTimer, QThread, QSocketNotifier
from PyQt5.QtWidgets import QWidgetItem, QFrame, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

def run():

    cwd = os.path.dirname(Pythonic.__file__)
    path = os.path.join(cwd, 'main_daemon.py')

    """
    if os.name == 'nt':
        Popen(['python', path, *sys.argv])
    else:
        print(sys.argv)
        Popen(['python3', path, *sys.argv])
    """
    if os.name == 'nt':
        Popen(['python', path, *sys.argv])
    else:
        print(sys.argv)
        #Popen(['python3', path, *sys.argv])
        app = QCoreApplication(sys.argv)

        timer = QTimer()
        timer.timeout.connect(lambda *args: None) # cathing signals outside the QT eventloop (e.g. SIGINT)
        timer.start(100)

        ex = MainWorker(app)
        ex.start(sys.argv)
    
        app.exec_()
