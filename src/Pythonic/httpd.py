from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from PySide2.QtCore import QRunnable


class HTTPD(QRunnable):

    def __init__(self):
        super(HTTPD, self).__init__()
        self.httpd = HTTPServer(('0.0.0.0', 7000), HTTP_Server)

    def run(self):

        self.httpd.serve_forever()

class HTTP_Server(BaseHTTPRequestHandler):

    #www_root = Path('html/static/')
    www_root    = Path('public_html/')
    def do_GET(self):

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
            self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
            self.end_headers()
            
            path = Path(__file__).parent / self.www_root / 'templates/PythonicWeb.html'

            self.wfile.write(open(path, 'rb').read())


        elif self.path == '/qtlogo.svg':
            open_path = Path.cwd() / self.www_root / 'qtlogo.svg'

            with open(open_path,'rb') as f:
                img_data = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.send_header('Content-length', str(len(img_data)))
            self.end_headers()

            self.wfile.write(img_data)
            
        elif self.path == '/favicon.ico':
            open_path = Path.cwd() / self.www_root / 'favicon.ico'

            with open(open_path,'rb') as f:
                img_data = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'image/vnd.microsoft.icon')
            self.send_header('Content-length', str(len(img_data)))
            self.end_headers()

            self.wfile.write(img_data)


        elif self.path == '/qtloader.js':
            open_path = Path.cwd() / self.www_root /  'qtloader.js'
            with open(open_path,'rb') as f:
                js_data = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
        
            self.wfile.write(js_data)

        elif self.path == '/CoolingSystem.js':
            open_path = Path.cwd() / self.www_root / 'CoolingSystem.js'
            with open(open_path,'rb') as f:
                js_data = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
        
            self.wfile.write(js_data)

        elif self.path == '/CoolingSystem.wasm':
            self.send_response(200)
            self.send_header('Content-type', 'application/wasm')
            self.end_headers()

            open_path = Path.cwd() / self.www_root / 'CoolingSystem.wasm'

            with open(open_path,'rb') as f:
                bin_data = f.read()

            self.wfile.write(bin_data)