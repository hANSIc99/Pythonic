import logging

class Function():

    def __init__(self, config, inputData, queue):
        logging.debug('Function.__init__()')
        self.config     = config
        self.inputData  = inputData
        self.queue = queue
        self.logger     = logging.getLogger() # mt only
        self.bStop      = False

    def __setstate__(self, state):
        logging.debug('__setstate__() called Function')
        self.config, self.inputData, self.queue, self.logger, self.bStop = state

    def __getstate__(self):
        logging.debug('__getstate__() called Function')
        return (self.config, self.inputData, self.queue, self.logger, self.bStop)

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

    def __init__(self, bComplete, data, message, exit=False):
        self.bComplete  = bComplete
        self.data       = data
        self.message    = message # Log message string
        
        # Becomes true if the record should not be passed to any child
        # Necessary to leave the ProcessHandler 
        self.exit       = exit 


    def __setstate__(self, state):
        #logging.debug('__setstate__() called Record')
        self.bComplete, self.data, self.message, self.exit = state

    def __getstate__(self):
        #logging.debug('__getstate__() called Record')
        return(self.bComplete, self.data, self.message, self.exit)