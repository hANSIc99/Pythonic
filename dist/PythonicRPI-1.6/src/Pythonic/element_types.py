import logging, pickle
from pathlib import Path


class Function():

    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        #logging.debug('Function.__init__()')
        self.id             = id
        self.config         = config
        self.inputData      = inputData
        self.return_queue   = return_queue
        self.cmd_queue      = cmd_queue
        self.logger         = logging.getLogger() # mt only
        self.bStop          = False

        self.logger.setLevel(logging.DEBUG)

    def __setstate__(self, state):
        #logging.debug('__setstate__() called Function')
        self.id, self.config, self.inputData, self.return_queue, self.cmd_queue, self.logger, self.bStop = state

    def __getstate__(self):
        #logging.debug('__getstate__() called Function')
        return (self.id, self.config, self.inputData, self.return_queue, self.cmd_queue, self.logger, self.bStop)

    def execute_ex(self):

        #logging.debug('execute_ex() called Function')

        try:
            result = self.execute()
        except Exception as e:
            self.logger.error(e)
            result = e

        return result

class Record():

    def __init__(self, data, message=None):

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

    def __init__(self, data, bStop=False):
        self.bStop  = bStop
        self.data   = data

    def __setstate__(self, state):
        #logging.debug('__setstate__() called Record')
        self.bStop, self.data = state

    def __getstate__(self):
        #logging.debug('__getstate__() called Record')
        return(self.bStop, self.data)


def storePersist(func):

    def wrapper(self, *args, **kwargs):

        func(self, *args, **kwargs)

        with open(self.filename, 'wb') as f:
            try:
                pickle.dump(self.copy(), f)
            except Exception as e:
                pass
        
    return wrapper


class ListPersist(list):

    def __init__(self, name: str) -> None:
        # BAUSTELLE
        self.filename = Path.home() / 'Pythonic' / 'executables' / '{}.obj'.format(name)

        if self.filename.exists():

            with open(self.filename, 'rb') as f:

                data = pickle.load(f)
                super().extend(data)



    def reload(self):

        if self.filename.exists():

            with open(self.filename, 'rb') as f:

                data = pickle.load(f)
                super().clear()
                super().extend(data)
                return True

        else:
            return False


    

    @storePersist
    def append(self, __object) -> None:
        return super().append(__object)

    @storePersist
    def extend(self, __iterable) -> None:
        return super().extend(__iterable)

    @storePersist
    def remove(self, __value) -> None:
        return super().remove(__value)

    @storePersist
    def pop(self, __index: int):
        return super().pop(__index=__index)

    @storePersist
    def clear(self) -> None:
        return super().clear()