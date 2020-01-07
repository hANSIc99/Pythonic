import eventlet, random, os
from eventlet import wsgi, websocket

@websocket.WebSocketWSGI
def handle(ws):
    if ws.path == '/echo':
        print('WS == \'/echo\'')
        while True:
            m = ws.wait()
            if m is None:
                break
            ws.send(m)
    elif ws.path == '/data':
        print('WS == \'/data\'')
        for i in range (10):
            ws.send('0 {} {}\n'.format(i, random.random()))
            eventlet.sleep(0.1)

#standard server
def dispatch(environ, start_response):
    if environ['PATH_INFO'] == '/data':
        print('PATH_INFO == \'/data\'')
        return handle(environ, start_response)
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
