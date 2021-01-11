import sys, logging, pickle, locale, datetime, os, signal, time, itertools, tty, termios, select
from element_types import Record, Function

    
class Element(Function):

    def __init__(self, config, inputData, return_queue, cmd_queue):
        super().__init__(config, inputData, return_queue, cmd_queue)


    def execute(self):

        """
        cnt = 0
        while True :
            time.sleep(1)

            # if cmdQueue.bStop BAUSTELLE
            if self.bStop:
                recordDone = Record(False, cnt, None, True) # Exit message
                # Necessary to end the ProcessHandler     
                self.queue.put(recordDone)
                break      


            recordDone = Record(False, cnt, None)     
            self.queue.put(recordDone)
            cnt += 1
    


        """
        #time.sleep(0.2)
        recordDone = Record(data="Hello from GenericPython", message='<<<<<<<>>>>>>>>> Message from {:04d}'.format(self.config['Identifier']))     
        self.return_queue.put(recordDone)



