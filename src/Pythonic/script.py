#!/usr/bin/python3

import eventlet, os, sys, logging
from Pythonic.web_daemon import MainWorker
from PySide2.QtCore import QCoreApplication, QTimer

print(os.path.dirname(os.path.realpath(__file__)))
print(os.path.dirname(__file__))
def run():

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda : None)
    app = QCoreApplication(sys.argv)
    
    ex = MainWorker(app)
    ex.start(sys.argv)
    
    app.exec_()
    """
    cwd = os.path.dirname(os.path.realpath(__file__))   

    cwd = os.path.dirname(Pythonic.__file__)
    path = os.path.join(cwd, 'main.py')

    if os.name == 'nt':
        Popen(['python', path])
    else:
        Popen(['python3', path])
    """

