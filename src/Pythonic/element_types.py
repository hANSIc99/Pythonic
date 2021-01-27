import logging



class Function():

    def __init__(self, config, inputData, return_queue, cmd_queue):
        #logging.debug('Function.__init__()')
        self.config         = config
        self.inputData      = inputData
        self.return_queue   = return_queue
        self.cmd_queue      = cmd_queue
        self.logger         = logging.getLogger() # mt only
        self.bStop          = False

    def __setstate__(self, state):
        #logging.debug('__setstate__() called Function')
        self.config, self.inputData, self.return_queue, self.cmd_queue, self.logger, self.bStop = state

    def __getstate__(self):
        #logging.debug('__getstate__() called Function')
        return (self.config, self.inputData, self.return_queue, self.cmd_queue, self.logger, self.bStop)

    def execute(self, input):
        #logging.debug('execute() called Function')

        result = None
        return result

    def execute_ex(self, input):

        #logging.debug('execute_ex() called Function')

        try:
            result = self.execute(input)
        except Exception as e:
            result = e

        return result

class Record():

    def __init__(self, data, message):

        self.data       = data
        self.message    = message # Log message string


    def __setstate__(self, state):
        #logging.debug('__setstate__() called Record')
        self.data, self.message = state

    def __getstate__(self):
        #logging.debug('__getstate__() called Record')
        return(self.data, self.message)

class GuiCMD:
    
    def __init__(self, text):
        self.text = text

    def __setstate__(self, state):
        self.text = state

    def __getstate__(self):
        return(self.text)


class ProcCMD:

    def __init__(self, bStop):
        self.bStop = bStop

    def __setstate__(self, state):
        #logging.debug('__setstate__() called Record')
        self.bStop = state

    def __getstate__(self):
        #logging.debug('__getstate__() called Record')
        return(self.bStop)