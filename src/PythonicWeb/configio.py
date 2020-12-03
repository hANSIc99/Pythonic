import os, logging, json
from PySide2.QtCore import QThread, Signal


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
        with open('PythonicWeb/config/current_config.json', 'r') as file:
            config = json.load(file)

        
        cmd = { 'cmd' : 'CurrentConfig',
                'data' : config }

        self.tooldataLoaded.emit(cmd)