import eventlet, os, sys, logging
from web_daemon import MainWorker
from PySide2.QtCore import QCoreApplication, QTimer
		
os.environ['PYTHONWARNINGS'] = 'ignore:semaphore_tracker:UserWarning'



def run():
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda : None)
    
    app = QCoreApplication(sys.argv)
    ex = MainWorker(app)
    #signal.signal(signal.SIGINT, ex.exitApp)
    ex.start(sys.argv)
    
    app.exec_()

    #listener = eventlet.listen(('127.0.0.1', 7000))
    #print('\nVisit http://localhost:7000/ in your websocket-capable browser.\n')
    #wsgi.server(listener, dispatch)



if __name__ == '__main__':

    run()
