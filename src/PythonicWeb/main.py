import eventlet, os, sys, logging
from eventlet import wsgi, websocket, greenthread
from web_daemon import MainWorker
from PyQt5.QtCore import QCoreApplication, QTimer
execTimer = False


@websocket.WebSocketWSGI
def startTimer(ws):
    n_cnt = 0
    global execTimer
    while execTimer:
        print('Timer fired! {}'.format(n_cnt))

        greenthread.sleep(1)
        n_cnt+=1

        try:
            ws.send('Timer fired! {}'.format(n_cnt))
        except Exception as e:
            print('Client websocket not available')
            ws.close()
            return

@websocket.WebSocketWSGI
def processMessage(ws):
    m = ws.wait()
    print('Message received: {}'.format(m))

       
@websocket.WebSocketWSGI
def saveData(ws):
    filename = ws.wait()
    print('Filename: {}'.format(filename))
    data = ws.wait()
    data_size = float(len(data)) / 1000 #kb
    print('Sizeof data: {:.1f} kb'.format(data_size))
    new_file = os.path.join(os.path.expanduser('~'), filename)
    print('Upload saved to: {}'.format(new_file))
    with open(new_file, 'wb') as file:
        file.write(data)


def dispatch(environ, start_response):

    """
        WEBSOCKETS
    """

    root_url = 'PythonicWeb/'
    global execTimer

    if environ['PATH_INFO'] == '/data':
        print('PATH_INFO == \'/data\'')
        return saveData(environ, start_response)
    elif environ['PATH_INFO'] == '/message':
        print('PATH_INFO == \'/message\'')
        return processMessage(environ, start_response)
    elif environ['PATH_INFO'] == '/timer':
        print('PATH_INFO == \'/timer\'')
        if execTimer:
            execTimer = False
            start_response('200 OK', [])
            return []
        else:
            execTimer = True
            return startTimer(environ, start_response)

        """
            STANDARD HTML ENDPOINTS
        """

    elif environ['PATH_INFO'] == '/':
        print('PATH_INFO == \'/\'')
        start_response('200 OK', [('content-type', 'text/html')])
        return [open(os.path.join(os.path.dirname(__file__),
            root_url + 'templates/PythonicWeb.html')).read()]
   
    elif environ['PATH_INFO'] == '/qtloader.js':
        print('PATH_INFO == \'/qtloader.js\'')
        str_data = open(os.path.join(os.path.dirname(__file__),
            root_url + 'static/qtloader.js')).read() 
        start_response('200 OK', [('content-type', 'application/javascript') ])

        return [str_data]

    elif environ['PATH_INFO'] == '/qtlogo.svg':
        print('PATH_INFO == \'/qtlogo.svg\'')
        img_data = open(os.path.join(os.path.dirname(__file__),
            root_url + 'static/qtlogo.svg'), 'rb').read() 
        start_response('200 OK', [('content-type', 'image/svg+xml'),
                                ('content-length', str(len(img_data)))])

        return [img_data]

    elif environ['PATH_INFO'] == '/PythonicWeb.js':
        print('PATH_INFO == \'/PythonicWeb.js\'')
        str_data = open(os.path.join(os.path.dirname(__file__),
            root_url + 'static/PythonicWeb.js')).read() 
        start_response('200 OK', [('content-type', 'application/javascript')])
        return [str_data]

    elif environ['PATH_INFO'] == '/PythonicWeb.wasm':
        print('PATH_INFO == \'/PythonicWeb.wasm\'')
        bin_data = open(os.path.join(os.path.dirname(__file__),
            root_url + 'static/PythonicWeb.wasm'), 'rb').read() 
        start_response('200 OK', [('content-type', 'application/wasm')])
        return [bin_data]		

    else:
        path_info = environ['PATH_INFO']
        print('PATH_INFO = {}'.format(path_info))
        return None
		

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
