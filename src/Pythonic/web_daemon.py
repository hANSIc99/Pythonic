import sys, logging, locale, datetime, os, signal, time, json, argparse
import multiprocessing as mp
from eventlet import wsgi, websocket, greenthread, listen
from threading import Timer, Thread, Event
from pathlib import Path
from zipfile import ZipFile
from enum import Enum
from shutil import copyfile
from PySide2.QtCore import QCoreApplication, QObject, QThread, Qt
from PySide2.QtCore import Signal

try:
    from logfile_hanlder import LogFileHandler
    from execution_operator import Operator   
    from screen import reset_screen, reset_screen_dbg
    from configio import ToolboxLoader, ConfigLoader, EditorLoader, ConfigWriter, ExecSysCMD
except ImportError:
    from Pythonic.logfile_hanlder import LogFileHandler
    from Pythonic.execution_operator import Operator
    from Pythonic.screen import reset_screen, reset_screen_dbg
    from Pythonic.configio import ToolboxLoader, ConfigLoader, EditorLoader, ConfigWriter, ExecSysCMD


##############################################
#                                            #
#                GLOBAL PATHS                #
#                                            #
##############################################

www_root    = 'public_html/'
www_static  = 'public_html/static/'
www_config  = 'public_html/config/'
executables = 'executables'


# Allow to quit with CTRL+C
signal.signal(signal.SIGINT, signal.SIG_DFL)


class LogLvl(Enum):
    DEBUG       = 0
    INFO        = 1
    WARNING     = 2
    CRITICAL    = 3
    FATAL       = 4

# Replace the websockets with QWebSockets
@websocket.WebSocketWSGI
def rcv(ws):

    #logging.getLogger()

    def send(command):
        #logging.debug('send() - command: {}'.format(command['cmd']))
        try:
            ws.send(json.dumps(command))
        except Exception as e:
            logging.info('PythonicWeb - RCV Socket connection lost: {}'.format(e))
            ws.environ['mainWorker'].frontendCtrl.disconnect(send)
 
    ws.environ['mainWorker'].frontendCtrl.connect(send)
    
    bConnected = True
    while bConnected:
        greenthread.sleep(0.1)
        QCoreApplication.processEvents()
        greenthread.sleep(0.1)
        QCoreApplication.processEvents()
        greenthread.sleep(0.1)
        QCoreApplication.processEvents()

        try:

            date = datetime.datetime.now() #.strftime("%d-%b-%Y")
            jsonHeartBeat = {   'cmd'       : 'Heartbeat',
                                'address'   : { 'target' : 'MainWindow'} ,
                                'data' : date.strftime("%d-%b-%Y %H:%M:%S") }

            ws.send(json.dumps(jsonHeartBeat))

        except Exception as e:
            logging.info('PythonicWeb - RCV Socket connection lost: {}'.format(e))
            ws.environ['mainWorker'].frontendCtrl.disconnect(send)
            bConnected = False

    logging.debug('PythonicWeb - RCV Socket closed')


@websocket.WebSocketWSGI
def ctrl(ws):
    logging.debug('PythonicDaemon - CTRL WebSocket connected')   
    while True:
        m = ws.wait()
        if m is None:
            logging.debug('PythonicDaemon - CTRL Socket Closed')            
            break;   
        else:

            msg = json.loads(m)
            
            logging.debug('PythonicWeb    - Command: {}'.format(msg['cmd']))

            if msg['cmd'] == 'logMsg':
                # logging
                logObj = msg['data']

                if logObj['logLvL'] == LogLvl.DEBUG.value:
                    logging.debug('PythonicWeb    - {}'.format(logObj['msg']))
                elif logObj['logLvL'] == LogLvl.INFO.value:
                    logging.info('PythonicWeb    - {}'.format(logObj['msg']))
                elif logObj['logLvL'] == LogLvl.WARNING.value:
                    logging.warning('PythonicWeb    - {}'.format(logObj['msg']))
                elif logObj['logLvL'] == LogLvl.CRITICAL.value:
                    logging.error('PythonicWeb    - {}'.format(logObj['msg']))
                elif logObj['logLvL'] == LogLvl.FATAL.value:
                    logging.critical('PythonicWeb    - {}q'.format(logObj['msg']))


            elif msg['cmd'] == 'writeConfig':
                logging.debug('Config loaded')
                # Save config to to memory
                ws.environ['mainWorker'].config = msg['data']
                # Save config to file
                ws.environ['mainWorker'].saveConfig.emit(msg['data'])
                # Update config at Operator
                ws.environ['mainWorker'].updateConfig.emit(msg['data'])

            elif msg['cmd'] == 'StartExec':
                #logging.info(h.heap())
                elementId = msg['data']      
                # Update config at Operator
                ws.environ['mainWorker'].updateConfig.emit(ws.environ['mainWorker'].config)
                # Start execution with element Id
                ws.environ['mainWorker'].startExec.emit(elementId)


            elif msg['cmd'] == 'StopExec':
                elementId = msg['data']
                ws.environ['mainWorker'].stopExec.emit(elementId)
                logging.debug('PythonicWeb    - {}'.format(msg['cmd']))
            elif msg['cmd'] == 'QueryConfig':
                logging.debug('PythonicWeb    - {}'.format(msg['cmd']))
                ws.environ['mainWorker'].loadConfig()
            elif msg['cmd'] == 'QueryToolbox':
                logging.debug('PythonicWeb    - {}'.format(msg['cmd']))
                ws.environ['mainWorker'].loadTools()
            elif msg['cmd'] == 'QueryEditorToolbox' :
                logging.debug('PythonicWeb    - {}'.format(msg['cmd']))
                addr        = msg['address']
                typeName    = msg['data']
                ws.environ['mainWorker'].loadEditorConfig(addr, typeName)
            elif msg['cmd'] == 'SysCMD' :
                logging.debug('PythonicWeb    - {}'.format(msg['cmd']))
                ws.environ['mainWorker'].sysCommand.emit(msg['data'])
            elif msg['cmd'] == 'QueryElementStates' :
                logging.debug('PythonicWeb    - {}'.format(msg['cmd']))
                ws.environ['mainWorker'].queryStates.emit()
            elif msg['cmd'] == 'StartAll' :
                logging.debug('PythonicWeb    - {}'.format(msg['cmd']))
                ws.environ['mainWorker'].startAll.emit(ws.environ['mainWorker'].config)
            elif msg['cmd'] == 'StopAll' :
                logging.debug('PythonicWeb    - {}'.format(msg['cmd']))
                ws.environ['mainWorker'].stopAll.emit()
            elif msg['cmd'] == 'KillAll' :
                logging.debug('PythonicWeb    - {}'.format(msg['cmd']))
                ws.environ['mainWorker'].killAll.emit()
        
        del msg
        del m
             
@websocket.WebSocketWSGI
def saveConfig(ws):
    filename = ws.wait()
    logging.info('Upload Config: Filename: {}'.format(filename))
    data = ws.wait()

    # Create a backup of existing config
    home_path = Path.home() / 'Pythonic'
    try:
        copyfile( (home_path / 'current_config.json'), (home_path / 'current_config.json.old'))
    except Exception as e:
        logging.warning('Exception during creating backlup: {}'.format(e))
        pass
    
    new_file = os.path.join(www_config, 'current_config.json')
    data_size = float(len(data)) / 1000 #kb
    logging.info('Sizeof Config: {:.1f} kb'.format(data_size))
    # Backup previous config

    logging.info('Upload saved to: {}'.format(home_path / 'current_config.json'))
    with open((home_path / 'current_config.json'), 'wb') as file:
        file.write(data)
    
    ws.environ['mainWorker'].loadConfig()

@websocket.WebSocketWSGI
def saveExecutable(ws):
    filename = ws.wait()
    logging.info('Upload Executable: Filename: {}'.format(filename))
    data = ws.wait()
    data_size = float(len(data)) / 1000 #kb
    logging.info('Sizeof Config: {:.1f} kb'.format(data_size))
    home_path = Path.home() / 'Pythonic'

    #new_file = os.path.join(executables, filename)
    logging.info('Upload saved to: {}'.format(home_path / executables / filename))


    with open(home_path / executables /filename, 'wb') as file:
        file.write(data)

def dispatch(environ, start_response):

    """
        WEBSOCKETS
    """

    png_req4 = environ['PATH_INFO'][-4:] # last 4 characters '.png'
    png_req3 = environ['PATH_INFO'][-3:] # last 4 characters '.js'

    if environ['PATH_INFO'] == '/ctrl':
        logging.debug('PythonicDaemon - Open CTRL WebSocket')     
        return ctrl(environ, start_response)
    elif environ['PATH_INFO'] == '/rcv':
        logging.debug('PythonicDaemon - Open RCV WebSocket')     
        return rcv(environ, start_response)

    elif environ['PATH_INFO'] == '/config':
        logging.debug('PythonicDaemon - Open Config WebSocket')  
        return saveConfig(environ, start_response)

    elif environ['PATH_INFO'] == '/executable':
        logging.debug('PythonicDaemon - Open Config WebSocket')  
        return saveExecutable(environ, start_response)

    elif environ['PATH_INFO'] == '/log':
        logging.debug('PythonicDaemon - Providing list of log files')  
        log_files = os.listdir(Path.home() / 'Pythonic' / 'log')
        log_files = '\n'.join(log_files)

        start_response('200 OK', [  ('content-type', 'text/plain; charset=utf-8') ])                              
        
        return [log_files]


        ###########################
        # STANDARD HTML ENDPOINTS #
        ###########################

    elif environ['PATH_INFO'] == '/':
        #logging.debug('PATH_INFO == \'/\'')
        
        start_response('200 OK', [  ('content-type', 'text/html'),
                                    ('Cross-Origin-Opener-Policy', 'same-origin'),
                                    ('Cross-Origin-Embedder-Policy', 'require-corp')])
        return [open(os.path.join(os.path.dirname(__file__),
            www_root + 'templates/PythonicWeb.html')).read()]


    elif environ['PATH_INFO'] == '/qtlogo.svg':
        #logging.debug('PATH_INFO == \'/qtlogo.svg\'')

        open_path = os.path.join(os.path.dirname(__file__), www_static + 'qtlogo.svg')

        with open(open_path,'rb') as f:
            img_data = f.read()

        start_response('200 OK', [('content-type', 'image/svg+xml'),
                                ('content-length', str(len(img_data)))])

        return [img_data]

    elif environ['PATH_INFO'] == '/favicon.ico':
        #logging.debug('PATH_INFO == \'/qtlogo.svg\'')

        open_path = os.path.join(os.path.dirname(__file__), www_static + 'python.ico')

        with open(open_path,'rb') as f:
            img_data = f.read()

        start_response('200 OK', [('content-type', 'image/vnd.microsoft.icon'),
                                ('content-length', str(len(img_data)))])

        return [img_data]
        

    # IMAGES (*.png)
    elif png_req4 == '.png':
        logging.debug('PATH_INFO == ' + environ['PATH_INFO'])
        
        open_path = os.path.join(os.path.dirname(__file__), www_static + environ['PATH_INFO'])

        with open(open_path,'rb') as f:
            img_data = f.read()
        
        start_response('200 OK', [('content-type', 'image/png'),
                                ('content-length', str(len(img_data)))])
        
        return [img_data]

    # JAVS SCRIPT (*.js)

    elif png_req3 == '.js':
        #logging.debug('PATH_INFO == ' + environ['PATH_INFO'])
        open_path = os.path.join(os.path.dirname(__file__), www_static + environ['PATH_INFO'])
        with open(open_path,'rb') as f:
            img_data = f.read()
      
        start_response('200 OK', [('content-type', 'application/javascript')])
        
        return [img_data]

    
    # Executable (*.py)

    elif png_req3 == '.py':
        #logging.debug('PATH_INFO == ' + environ['PATH_INFO'])
        open_path = Path.home() / 'Pythonic' / 'executables' / environ['PATH_INFO'][1:]
        with open(open_path,'rb') as f:
            py_file = f.read()
      
        start_response('200 OK', [('content-type', 'application/javascript')])
        
        return [py_file]
    

    elif environ['PATH_INFO'] == '/PythonicWeb.wasm':
        #logging.debug('PATH_INFO == \'/PythonicWeb.wasm\'')

        open_path = os.path.join(os.path.dirname(__file__), www_static + 'PythonicWeb.wasm')

        with open(open_path,'rb') as f:
            bin_data = f.read()

        start_response('200 OK', [('content-type', 'application/wasm')])
        return [bin_data]	

    elif environ['PATH_INFO'] == '/PythonicWeb.data':
        #logging.debug('PATH_INFO == \'/PythonicWeb.data\'')

        open_path = os.path.join(os.path.dirname(__file__), www_static + 'PythonicWeb.data')

        with open(open_path,'rb') as f:
            bin_data = f.read()

        start_response('200 OK', [('content-type', 'application/wasm')])
        return [bin_data]	

    elif png_req4 == '.txt': # Log files
        #logging.debug('PATH_INFO == \'/PythonicWeb.wasm\'')

        open_path = Path.home() / 'Pythonic' / 'log' / environ['PATH_INFO'][1:]
        
        with open(open_path,'rb') as f:
            log_data = f.read()

        start_response('200 OK', [  ('content-type', 'text/plain; charset=utf-8')])                                                                   
                                                 
        return [log_data]

    # Config file (*.json)

    elif environ['PATH_INFO'] == '/current_config.json':
        #logging.debug('PATH_INFO == ' + environ['PATH_INFO'])
        open_path = Path.home() / 'Pythonic' / 'current_config.json'
        with open(open_path,'rb') as f:
            config_file = f.read()
      
        start_response('200 OK', [  ('content-type', 'application/json; charset=utf-8')])
        
        return [config_file]

    else:
        path_info = environ['PATH_INFO']
        logging.debug('PATH_INFO = {}'.format(path_info))
        return None


class WSGI_Server(QThread):

    def __init__(self, mainWorker):
        super().__init__()
        self.mainWorker = { 'mainWorker' : mainWorker }

    def run(self):

        #listener = eventlet.listen(('127.0.0.1', 7000))
        listener = listen(('0.0.0.0', 7000))
        wsgi.server(listener, dispatch, log_output=False, environ=self.mainWorker)


class MainWorker(QObject):

    kill_all        = Signal()
    

    max_grid_size   = 50
    max_grid_cnt    = 5
    config          = None # element configuration

    updateLogdate  = Signal(object)        # update displayed date string in stdin_reader
    updateConfig   = Signal(object)        # update configuration in execution operator
    startExec       = Signal(object)        # element-Id
    stopExec        = Signal(object)        # element-Id
    saveConfig      = Signal(object)        # configuration
    sysCommand      = Signal(object)        # Optional: Element Constructor / Destructor
    frontendCtrl    = Signal(object)
    queryStates     = Signal()              # Query the running states of elements
    startAll        = Signal(object)        # Start all elements: (config)
    stopAll         = Signal()              # Stop all elements
    killAll         = Signal()              # Kill all running processes

    def __init__(self, app):
        super(MainWorker, self).__init__()
        self.app = app

        # Setup command line arguments
        
        parser = argparse.ArgumentParser(description='Pythonic background daemon')
        # Debug output switch 
        parser.add_argument('-Ex', action='store_true', help='Interactive shell interface, Unix only')
        # Log level
        parser.add_argument('-v', action='store_true', help='Verbose output')

        self.args = parser.parse_args()

        # Set Log Level
        if self.args.v:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        # Instantiate the LogFileHandler
        self.logFileHandler = LogFileHandler(log_level)

        # Select multiprocessing spawn method
        mp.set_start_method('spawn')
        
        # Set working directory
        os.chdir(Path(__file__).parent.absolute())

        # Setup format
        locale.setlocale(locale.LC_TIME, '')

        # Instantiate WSGI Server
        self.wsgi_server = WSGI_Server(self)
        
        # Instantiate Execution Operator
        self.operator = Operator()
        self.operator.command.connect(self.forwardCmd)
        self.startExec.connect(self.operator.startExec)
        self.stopExec.connect(self.operator.stopExec)
        self.updateConfig.connect(self.operator.updateConfig)
        self.queryStates.connect(self.operator.getElementStates)
        self.startAll.connect(self.operator.startAll)
        self.stopAll.connect(self.operator.stopAll)
        self.killAll.connect(self.operator.killAll)
        

        # Instantiate Standard Input Reader (Unix only)
        if self.args.Ex:
            try:
                from stdin_reader import stdinReader
            except ImportError:
                from Pythonic.stdin_reader import stdinReader        
        
            self.stdinReader = stdinReader(self.operator.processHandles.items(), self.logFileHandler.log_date_str)
            self.stdinReader.quit_app.connect(self.exitApp)


        # Connect the logger
        if self.args.Ex:
            self.logFileHandler.updateLogdate.connect(self.stdinReader.updateLogDate)
               

        # Instantiate ToolboxLoader
        self.toolbox_loader = ToolboxLoader()
        self.toolbox_loader.tooldataLoaded.connect(self.forwardCmd)
        
        # Instantiate (Element)-EditorLoader

        self.editor_loader = EditorLoader()
        self.editor_loader.editorLoaded.connect(self.forwardCmd)
        
        # Instantiate ConfigWriter
        self.config_writer = ConfigWriter()
        self.config_writer.configSaved.connect(self.forwardCmd)
        self.saveConfig.connect(self.config_writer.saveConfig)

        # Instantiate ConfigLoader
        self.config_loader = ConfigLoader()
        self.config_loader.configLoaded.connect(self.configLoaded)

        # Instantiate System Command Executor
        self.exec_sys_cmd = ExecSysCMD()
        self.sysCommand.connect(self.exec_sys_cmd.execCommand)
            
    
    def exitApp(self):
        print('# Stopping all processes....')
        self.kill_all.emit()
        time.sleep(3) # wait for 1 seconds to kill all processes
        self.app.quit()
        os.kill(self.app.applicationPid(), signal.SIGTERM) # kill all related threads
    

    def start(self, args):

        
        reset_screen()    

        if self.args.Ex:
            reset_screen_dbg()    
            self.stdinReader.start() # call run() method in separate thread

        self.config = self.config_loader.loadConfigSync()


        self.wsgi_server.start()
        self.operator.start(self.config)

    def loadTools(self): # Multithreaded
        
        logging.debug('MainWorker::loadTools() called')
        self.toolbox_loader.start()

    def loadEditorConfig(self, address, typeName): # Multithreaded
        
        logging.debug('MainWorker::loadEditorConfig() called')
        self.editor_loader.startLoad(address, typeName)

    def forwardCmd(self, cmd):

        #logging.debug('MainWorker::forwardCmd() called')
        self.frontendCtrl.emit(cmd)

    def loadConfig(self): # Multithreaded
        
        logging.debug('MainWorker::loadConfig() called')
        self.config_loader.start()
           
    def configLoaded(self, config):

        self.config = config

        address = { 'target' : 'MainWindow'}
        
        cmd = { 'cmd'       : 'CurrentConfig',
                'address'   : address,
                'data'      : config }

        self.frontendCtrl.emit(cmd)

    def checkArgs(self, args):

        b_file_found = False
        grid_file = None

        for argument in args:
            if argument[0] == '-' or argument[0] == '--':
                print('Option found: {}'.format(argument))
            else:
                if not b_file_found:
                    b_file_found = True
                    grid_file = argument

        return grid_file
