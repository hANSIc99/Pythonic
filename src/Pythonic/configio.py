import os, logging, json
from datetime import datetime
from threading import Semaphore, Lock

from PySide2.QtCore import QThread, QObject, Signal, QMutex

class ExecSysCMD(QThread):

    cmd = None

    def __init__(self):
        super().__init__()

    def execCommand(self, cmd):
        self.cmd = cmd
        self.start()

    def run(self):

        logging.debug('ExecSysCMD::run() called')
        os.system(self.cmd)


class ConfigWriter(QThread):

    config      = None
    configSaved = Signal(object)   
    mutex       = QMutex()

    def __init__(self):
        super().__init__()
        self.www_config = '/public_html/config'
        self.cwd = os.path.dirname(__file__)

    def saveConfig(self, config):

        self.mutex.lock()
        self.config = config
        self.mutex.unlock()
        self.start()
    
    def run(self):

        logging.debug('ConfigWriter::saveConfig() called')

        self.mutex.lock()
        with open(os.path.join(self.cwd + self.www_config + 'current_config.json'), 'w') as file:
            json.dump(self.config, file, indent=4)

        self.mutex.unlock()
        last_saved = "Config last saved: " + datetime.now().strftime('%H:%M:%S')

        cmd = {  'cmd'       : 'SetInfoText',
                 'data'      : last_saved,
                 'address'   : {"target" : "MainWindow"}}

        self.configSaved.emit(cmd)


class EditorLoaderThread(QThread):

    editorLoaded        = Signal(object)

    def __init__(self, address, typeName):
        super().__init__()

        self.address    = address
        self.typeName   = typeName + '.editor'
        self.www_config = '/public_html/config/Toolbox'
        self.cwd = os.path.dirname(__file__)



    def run(self):

        logging.debug('EditorLoader::run() called')
        config = None
        bFound = False

        for dirpath, dirnames, filenames in os.walk(os.path.join(self.cwd + self.www_config)):
            if self.typeName in filenames:

                try:
                    with open(os.path.join(dirpath ,self.typeName), 'r') as file:

                        config = json.load(file)

                
                    cmd = { 'cmd' : 'ElementEditorConfig',
                            'address'   : self.address,
                            'data'      : config }
                    
                    logging.debug('EditorLoader::run() config loaded')
                    bFound = True
                    self.editorLoaded.emit(cmd)
                    #sleep(1)

                except Exception as e:
                    logging.warning('EditorLoader::run() - error opening file: {}'.format(e))
                
                
                break
            
                

        if not bFound:
            logging.warning('EditorLoader::run() - editor config file {} not found'.format(self.typeName))

    

class EditorLoader(QObject):

    editorLoaded        = Signal(object)

    typeName    = None
    address     = None

    threadList = []

    def __init__(self):
        super().__init__()
        self.cwd = os.path.dirname(__file__)

    def startLoad(self, address, typeName):

        logging.debug('EditorLoader::startLoad() - called')

        newThread   = EditorLoaderThread(address, typeName)
        newThread.editorLoaded.connect(self.fwrdCmd)
        newThread.finished.connect(self.cleanupThreadList)


        self.threadList.append(newThread)

        newThread.start()

    def fwrdCmd(self, cmd):
        self.editorLoaded.emit(cmd)

    def cleanupThreadList(self):
        # Remove finished threads from memory
        #i = 5

        # BAUSTELLE
        # If the threads are not removed from the list it will cause a memory leak
        # If the threads are removed from list it will cause a QThread Exception:
        # QThread: Destroyed while thread is still running
        #self.threadList[:] = [thread for thread in self.threadList if not thread.isRunning() ]
        for thread in self.threadList:
            x = thread
            if not thread.isRunning():
                self.threadList.remove(thread)
                x.editorLoaded.disconnect(self.fwrdCmd)
                x.finished.disconnect(self.cleanupThreadList)
                x.deleteLater()
     
        

class ToolboxLoader(QThread):

    tooldataLoaded      = Signal(object)

    def __init__(self):
        super().__init__()
        self.www_config = '/public_html/config'
        self.cwd = os.path.dirname(__file__)

    def run(self):

        logging.debug('ToolboxLoader::run() called')
        
        toolDirs = [ f for f in os.scandir(os.path.join(self.cwd + self.www_config + '/Toolbox/')) if f.is_dir() ]
        elements = [(d, f) for d in toolDirs for f in os.listdir(d.path) if f.endswith('.json')]
        elementsJSON = []
        
        for d, f in elements:
            
            filepath = os.path.join(d.path, f)
            e = None
            with open(filepath, 'r') as file:
                e = json.load(file)

            element = { 'assignment' : d.name,
                        'config' : e}

            elementsJSON.append(element)
            #logging.debug('MainWorker::loadTools() called')

        address = { 'target' : 'MainWindow'}

        cmd = { 'cmd'       : 'Toolbox',
                'address'   : address,
                'data'      : elementsJSON }
        
        self.tooldataLoaded.emit(cmd)


class ConfigLoader(QThread):

    tooldataLoaded      = Signal(object)

    def __init__(self):
        super().__init__()
        self.www_config = '/public_html/config'
        self.cwd = os.path.dirname(__file__)

    def run(self):


        config = None
        try:
            with open(os.path.join(self.cwd + self.www_config + 'current_config.json'), 'r') as file:
                config = json.load(file)

            address = { 'target' : 'MainWindow'}
            
            cmd = { 'cmd'       : 'CurrentConfig',
                    'address'   : address,
                    'data'      : config }

            self.tooldataLoaded.emit(cmd)
        except Exception as e:
            logging.warning('ConfigLoader::run() - no config found yet')

