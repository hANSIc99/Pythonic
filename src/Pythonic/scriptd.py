#!/usr/local/bin/python3

import os, sys, Pythonic
from subprocess import Popen

def run():
    if os.name == 'nt':
        Popen(['python', 'main_daemon.py', *sys.argv], cwd= os.path.dirname(Pythonic.__file__))
    else:
        Popen(['python3', 'main_daemon.py', *sys.argv], cwd= os.path.dirname(Pythonic.__file__))

