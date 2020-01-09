import eventlet, random, os
from time import sleep
from eventlet import wsgi, websocket, tpool

"""
def startTimer(ws):
    n_cnt = 0
    while True:
        print('Loop started!')
        #while True:
        sleep(2)
        n_cnt+=1
        ws.send('Timer executed: {}'.format(n_cnt))
"""


@websocket.WebSocketWSGI
def startTimer(ws):
    n_cnt = 0
    while True:
        print('Loop! {}'.format(n_cnt))
        """ waiting for messages
        m = ws.wait()
        if m is None:
            break
        """
        #while True:
        ws.send('Timer triggered: {}'.format(n_cnt))
        sleep(2)
        n_cnt+=1

@websocket.WebSocketWSGI
def handle(ws):
    if ws.path == '/echo':
        print('WS == \'/echo\'')
        while True:
            m = ws.wait()
            if m is None:
                break
            print('Message received: {}'.format(str(m)))
            ws.send(m)
    elif ws.path == '/data':
        print('WS == \'/data\'')
        while True:
            m = ws.wait()
            if m is None:
                break
            print('Message received: {}'.format(str(m)))

def dispatch(environ, start_response):
    if environ['PATH_INFO'] == '/data':
        print('PATH_INFO == \'/data\'')
        return handle(environ, start_response)
    elif environ['PATH_INFO'] == '/echo':
        print('PATH_INFO == \'/echo\'')
        return handle(environ, start_response)
    elif environ['PATH_INFO'] == '/timer':
        print('PATH_INFO == \'/timer\'')
        tpool.execute(startTimer, environ, start_response)
        return


    elif environ['PATH_INFO'] == '/wasm':
        print('PATH_INFO == \'/wasm\'')
        start_response('200 OK', [('content-type', 'text/html')])
        return [open(os.path.join(os.path.dirname(__file__),
            'PythonicWeb/templates/PythonicWeb.html')).read()]
    else:
        print('PATH_INFO == \'/\'')
        start_response('200 OK', [('content-type', 'text/html')])
        return [open(os.path.join(os.path.dirname(__file__),
            'websocket.html')).read()]

if __name__ == '__main__':
    listener = eventlet.listen(('127.0.0.1', 7000))
    print('\nVisit http://localhost:7000/ in your websocket-capable browser.\n')
    wsgi.server(listener, dispatch)
