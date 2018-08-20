#!/usr/local/bin/python3

import sys, os, Pythonic 

def run():
    print('Python starts at {}'.format(sys.prefix))
    os.chdir(os.path.dirname(Pythonic.__file__))
    print('Folder changed to {}'.format(os.getcwd()))
    from Pythonic import main
    main.run()

