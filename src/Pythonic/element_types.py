import logging, pickle
from pathlib import Path
from typing import Optional



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
            guiexc = GuiException(e)
            self.return_queue.put(guiexc)


class Record():

    def __init__(self, data : any, message : Optional[str] = None) -> None:

        self.data       = data # Will be passed to subsequent elements, even it is None
        self.message    = message # Log message string


    def __setstate__(self, state):
        #logging.debug('__setstate__() called Record')
        self.data, self.message = state

    def __getstate__(self):
        #logging.debug('__getstate__() called Record')
        return(self.data, self.message)


class PythonicError:

    def __init__(self, msg : str) -> None:
        self.msg = msg
    
    def  __str__(self) -> str:
        return 'Error: {}'.format(self.msg)


class GuiCMD:
    
    def __init__(self, text):
        self.text = text

    def __setstate__(self, state):
        self.text = state

    def __getstate__(self):
        return(self.text)


class GuiException:

    def __init__(self, e : Exception) -> None:
        self.e = e


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


class SetPersist(set):

    def __init__(self, name: str) -> None:

        self.filename = Path.home() / 'Pythonic' / 'executables' / '{}.obj'.format(name)

        if self.filename.exists():

            with open(self.filename, 'rb') as f:

                data = pickle.load(f)
                super().update(data)



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
    def add(self, __object) -> None:
        return super().add(__object)

    @storePersist
    def discard(self, __object) -> None:
        return super().discard(__object)

    @storePersist
    def pop(self) -> None:
        return super().pop()

    @storePersist
    def clear(self) -> None:
        return super().clear()