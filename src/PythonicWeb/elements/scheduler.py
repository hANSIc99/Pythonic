import sys, logging, pickle, datetime, os, signal, time, itertools, tty, termios, select

class Function():

    def __init__(self, config, b_debug=False):
        logging.debug('Function.__init__()')
        self.config = config
        self.b_debug = b_debug
        logger = logging.getLogger()

    def __setstate__(self, state):
        logging.debug('__setstate__() called Function')
        self.config, self.b_debug, = state

    def __getstate__(self):
        logging.debug('__getstate__() called Function')
        return (self.config, self.b_debug)

    def execute(self, input):
        logging.debug('execute() called Function')

        result = None
        return result

    def execute_ex(self, input):

        logging.debug('execute_ex() called Function')

        try:
            result = self.execute(input)
        except Exception as e:
            result = e

        return result

    
class Element(Function):

    def __init__(self, config, b_debug=False):
        super().__init__(config, b_debug)


    def execute(self, input):
        while True:
            time.sleep(1)
            logging.debug("Scheduler Called")