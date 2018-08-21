#!/usr/local/bin/python3

import sys, os, Pythonic 
from subprocess import Popen

def run():
    print('Python starts at {}'.format(sys.prefix))
    Popen(['python3', 'main.py'], cwd= os.path.dirname(Pythonic.__file__))

