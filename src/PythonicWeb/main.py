import eventlet, os, sys, logging
from web_daemon import MainWorker
from PySide2.QtCore import QCoreApplication, QTimer
		

if __name__ == '__main__':

    log_level = logging.DEBUG
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')
    logger = logging.getLogger()

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda : None)
    app = QCoreApplication(sys.argv)
    
    ex = MainWorker(app)
    ex.start(sys.argv)
    
    app.exec_()

    #listener = eventlet.listen(('127.0.0.1', 7000))
    #print('\nVisit http://localhost:7000/ in your websocket-capable browser.\n')
    #wsgi.server(listener, dispatch)
