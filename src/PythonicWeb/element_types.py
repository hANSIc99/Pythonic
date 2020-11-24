import logging

class Function():

    def __init__(self, config, inputData, returnPipe):
        logging.debug('Function.__init__()')
        self.config     = config
        self.inputData  = inputData
        self.returnPipe = returnPipe
        self.logger     = logging.getLogger() # mt only

    def __setstate__(self, state):
        logging.debug('__setstate__() called Function')
        self.config, self.inputData, self.returnPipe, self.logger, = state

    def __getstate__(self):
        logging.debug('__getstate__() called Function')
        return (self.config, self.inputData, self.returnPipe, self.logger)

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

class Record():

    def __init__(self, bComplete, data, message):
        self.bComplete  = bComplete
        self.data      = data
        self.message    = message

    def __setstate__(self, state):
        #logging.debug('__setstate__() called Record')
        self.bComplete, self.data, self.message = state

    def __getstate__(self):
        #logging.debug('__getstate__() called Record')
        return(self.bComplete, self.data, self.message)