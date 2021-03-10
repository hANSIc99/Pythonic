import os, logging, json
from copy import deepcopy
from shutil import copyfile
from datetime import datetime
from pathlib import Path
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

        if os.name == 'nt' and self.cmd['Win32'] != '':
            os.system(self.cmd['Win32'])
        elif self.cmd['Unix'] != '':
            os.system(self.cmd['Unix'])



class ConfigWriter(QThread):

    config      = None
    configSaved = Signal(object)   
    mutex       = QMutex()

    def __init__(self):
        super().__init__()
        self.cfg_file = Path.home() / 'Pythonic' / 'current_config.json'

    def saveConfig(self, config):

        self.mutex.lock()
        self.config = deepcopy(config)
        self.mutex.unlock()
        self.start()
    
    def run(self):

        logging.debug('ConfigWriter::saveConfig() called')

        self.mutex.lock()
        try:
            with open( self.cfg_file, 'w') as file:
                json.dump(self.config, file, indent=4)
        except Exception as e:
            logging.debug('ConfigWriter::saveConfig() - {}'.format(e))
            pass
            return
            


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
        self.editorPath = Path(__file__).parent.absolute() / 'public_html' / 'config' / 'Toolbox'


    def run(self):

        logging.debug('EditorLoader::run() called')
        config = None
        bFound = False

        for dirpath, dirnames, filenames in os.walk(self.editorPath):
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
        self.toolBoxPath = Path(__file__).parent.absolute() / 'public_html' / 'config' / 'Toolbox'

    def run(self):

        logging.debug('ToolboxLoader::run() called')
        
        #toolDirs = [ f for f in os.scandir(os.path.join(self.cwd + self.www_config + '/Toolbox/')) if f.is_dir() ]
        toolDirs = [ f for f in os.scandir(self.toolBoxPath) if f.is_dir() ]
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
        self.home_path  = Path.home() / 'Pythonic'
        self.cfg_file   = self.home_path  / 'current_config.json'

    def run(self):

        config = None
        self.loadConfig()

    def loadConfig(self, bRecover=False):

        try:
            with open(self.cfg_file, 'r') as file:
                config = json.load(file)

            address = { 'target' : 'MainWindow'}
            
            cmd = { 'cmd'       : 'CurrentConfig',
                    'address'   : address,
                    'data'      : config }

            self.tooldataLoaded.emit(cmd)
            if(bRecover):
                logging.warning('Old config restored successfully')

        except Exception as e:
            
            # Return if an exception occured when already tried
            # to recover the old config
            if(bRecover):
                logging.warning('>>> No config file found')
                return

            logging.warning('ConfigLoader::run() - Exception: {}'.format(e))
            logging.warning('>>> Check if backup exists')

            try:
                copyfile( (self.home_path / 'current_config.json.old'), (self.home_path / 'current_config.json'))
            except Exception as e:
                logging.warning('Exception restoring backlup: {}'.format(e))
                pass

            self.loadConfig(bRecover=True)
