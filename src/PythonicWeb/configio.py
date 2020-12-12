import os, logging, json
from PySide2.QtCore import QThread, Signal


class EditorLoader(QThread):

    editorLoaded        = Signal(object)

    typeName    = None
    address     = None

    def __init__(self,):
        super().__init__()


    def startLoad(self, address, typeName):

        logging.debug('EditorLoader::startLoad() - called')
        self.address  = address
        self.typeName = typeName + '.editor'
        self.start()

    def run(self):

        logging.debug('EditorLoader::run() called')
        config = None

        for dirpath, dirnames, filenames in os.walk('PythonicWeb/config/Toolbox/'):
            if self.typeName in filenames:

                try:
                    with open(os.path.join(dirpath ,self.typeName), 'r') as file:

                        config = json.load(file)

                
                    cmd = { 'cmd' : 'ElementEditorConfig',
                            'data' : config }
                    logging.debug('EditorLoader::run() config loaded')
                    self.editorLoaded.emit(cmd)
                except Exception as e:
                    logging.warning('EditorLoader::run() - error opening file: {}'.format(e))
                
                
                break


        
        

class ToolboxLoader(QThread):

    tooldataLoaded      = Signal(object)

    def __init__(self):
        super().__init__()


    def run(self):

        #toolDirs = glob('PythonicWeb/config/Toolbox/*/')
        #toolDirs = glob(os.path.join('PythonicWeb/config/Toolbox/',"*", ""))
        logging.debug('ToolboxLoader::run() called')
        toolDirs = [ f for f in os.scandir('PythonicWeb/config/Toolbox/') if f.is_dir() ]
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

        
        cmd = { 'cmd' : 'Toolbox',
                'data' : elementsJSON }
        
        self.tooldataLoaded.emit(cmd)


class ConfigLoader(QThread):

    tooldataLoaded      = Signal(object)

    def __init__(self):
        super().__init__()
    
    
    def run(self):


        config = None
        try:
            with open('PythonicWeb/config/current_config.json', 'r') as file:
                config = json.load(file)

        
            cmd = { 'cmd' : 'CurrentConfig',
                    'data' : config }

            self.tooldataLoaded.emit(cmd)
        except Exception as e:
            logging.warning('ConfigLoader::run() - no config found yet')

