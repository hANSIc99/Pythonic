#!/usr/bin/python3

import os, sys, json
import debugpy
from pathlib import Path
from Pythonic.web_daemon import MainWorker
from PySide2.QtCore import QCoreApplication, QTimer


debugpy.configure({"subProcess": True})
debugpy.listen(5678)


def run():


    # Create home path (if not already existing)
    
    home_path = Path.home() / 'Pythonic'
    home_path.mkdir(exist_ok=True)

    # Create log path (if not already existing)

    logPath = home_path / 'log'
    logPath.mkdir(exist_ok=True)

    # Create directory for executables (if not already existing)

    execPath = home_path / 'executables'
    execPath.mkdir(exist_ok=True)

    # Create directory for vs code configuration (if not already existing)

    vsCodepath = execPath / '.vscode' 
    vsCodepath.mkdir(exist_ok=True)

    # Append executables folder to module search path
    sys.path.append(str(execPath))


    """
    Create launch.json with current PID in hte libraries installation path
    """
    libPath = os.path.dirname(__file__)

    Path(os.path.join(libPath, '.vscode/')).mkdir(exist_ok=True)

    launch = {  "version": "0.2.0",
                "configurations": [
            {
                "name": "Pythonic: Attach",
                "type": "python",
                "request": "attach",
                "justMyCode": False,
                "connect" : {
                    "host" : "localhost",
                    "port"  : 5678
                }
            }
        ]
    }

    with open(os.path.join(libPath + '/.vscode/launch.json'), 'w') as file:
        json.dump(launch, file, indent=4)



    """
    Create launch.json with current PID in the user executables path
    """
    
    with open(vsCodepath / 'launch.json', 'w') as file:
        json.dump(launch, file, indent=4)
    


    app = QCoreApplication(sys.argv)
    
    ex = MainWorker(app)
    ex.start(sys.argv)
    
    app.exec_()

if __name__ == '__main__':

    run()