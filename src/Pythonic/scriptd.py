#!/usr/local/bin/python3

import os, sys, Pythonic
from Pythonic.main_daemon import MainWorker
from PyQt5.QtCore import QCoreApplication, QTimer

def run():

    app = QCoreApplication(sys.argv)
    
    timer = QTimer()
    timer.timeout.connect(lambda *args: None) # cathing signals outside the QT eventloop (e.g. SIGINT)
    timer.start(100)

    ex = MainWorker(app)
    ex.start(sys.argv)
    
    app.exec_()
