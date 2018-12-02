#!/usr/local/bin/python3

import sys, os, Pythonic 
from subprocess import Popen

def run():
    if os.name == 'nt':
        Popen(['python', 'main.py'], cwd= os.path.dirname(Pythonic.__file__))
    else:
        Popen(['python3', 'main.py'], cwd= os.path.dirname(Pythonic.__file__))

