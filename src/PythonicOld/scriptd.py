#!/usr/local/bin/python3

import os, sys, Pythonic
from Pythonic.main_daemon import MainWorker
from PyQt5.QtCore import QCoreApplication, QTimer

def run():

    app = QCoreApplication(sys.argv)
    
    ex = MainWorker(app)
    ex.start(sys.argv)
    
    app.exec_()
