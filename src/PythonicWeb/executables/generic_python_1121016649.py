import sys, logging, pickle, locale, datetime, os, signal, time, itertools, tty, termios, select
from element_types import Record, Function

    
class Element(Function):

    def __init__(self, config, inputData, queue):
        super().__init__(config, inputData, queue)


    def execute(self):


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



