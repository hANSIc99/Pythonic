#!/usr/bin/python3

import os, sys, logging, json
from pathlib import Path
from Pythonic.web_daemon import MainWorker
from PySide2.QtCore import QCoreApplication, QTimer




def run():

    """
    Create launch.json with current PID
    """
    cwd = os.path.dirname(__file__)

    Path(os.path.join(cwd, '.vscode/')).mkdir(exist_ok=True)

    launch = {  "version": "0.2.0",
                "configurations": [
            {
                "name"      : "Pythonic: Attach",
                "type"      : "python",
                "request"   : "attach",
                "processId" : os.getpid(),
                "justMyCode": False,
                "cwd"       : cwd
            }
        ]
    }

    with open(os.path.join(cwd + '/.vscode/launch.json'), 'w') as file:
        json.dump(launch, file, indent=4)

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda : None)
    app = QCoreApplication(sys.argv)
    
    ex = MainWorker(app)
    ex.start(sys.argv)
    
    app.exec_()