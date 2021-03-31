#!/usr/bin/python3

import os, sys, logging, json
from pathlib import Path
from Pythonic.web_daemon import MainWorker
from PySide2.QtCore import QCoreApplication, QTimer




def run():

    """
    Create launch.json with current PID in hte libraries installation path
    """
    libPath = os.path.dirname(__file__)
    

    Path(os.path.join(libPath, '.vscode/')).mkdir(exist_ok=True)

    launch = {  "version": "0.2.0",
                "configurations": [
            {
                "name"      : "Pythonic: Attach",
                "type"      : "python",
                "request"   : "attach",
                "processId" : os.getpid(),
                "justMyCode": False,
               "cwd"       : libPath
            }
        ]
    }

    with open(os.path.join(libPath + '/.vscode/launch.json'), 'w') as file:
        json.dump(launch, file, indent=4)

    """
    Create launch.json with current PID in the user executables path
    """

    userDir = Path.home() / 'Pythonic' / 'executables' / '.vscode' 
    
    Path(userDir).mkdir(exist_ok=True)

    
    with open(userDir / 'launch.json', 'w') as file:
        json.dump(launch, file, indent=4)
    


    app = QCoreApplication(sys.argv)
    
    ex = MainWorker(app)
    ex.start(sys.argv)
    
    app.exec_()

if __name__ == '__main__':

    run()