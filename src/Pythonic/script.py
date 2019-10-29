#!/usr/local/bin/python3

import sys, os, Pythonic 
from subprocess import Popen

def run():

    if os.name == 'nt':
        Popen(['python', 'main.py'], cwd= os.path.dirname(Pythonic.__file__))
    else:
        Popen(['python3', 'main.py'], cwd= os.path.dirname(Pythonic.__file__))
        
    """ BAUSTELLE

    cwd = os.path.dirname(Pythonic.__file__)
    path = os.path.join(cwd, 'main.py')
    if os.name == 'nt':
        Popen(['python', path])
    else:
        Popen(['python3', path])
    """

