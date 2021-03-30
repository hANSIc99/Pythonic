import eventlet, os, sys, logging
from web_daemon import MainWorker
from PySide2.QtCore import QCoreApplication, QTimer
		
os.environ['PYTHONWARNINGS'] = 'ignore:semaphore_tracker:UserWarning'



def run():
    
    app = QCoreApplication(sys.argv)
    ex = MainWorker(app)
    ex.start(sys.argv)
    
    app.exec_()

if __name__ == '__main__':

    run()
