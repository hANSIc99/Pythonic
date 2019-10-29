#!/usr/local/bin/python3

import os, sys, Pythonic
from subprocess import Popen

def run():
    cwd = os.path.dirname(Pythonic.__file__)
    path = os.path.join(cwd, 'main_daemon.py')

    if os.name == 'nt':
        Popen(['python', path, *sys.argv])
    else:
        print(sys.argv)
        Popen(['python3', path, *sys.argv])
