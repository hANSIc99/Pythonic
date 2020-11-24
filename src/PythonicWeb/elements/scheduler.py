import sys, logging, pickle, datetime, os, signal, time, itertools, tty, termios, select
from element_types import Record, Function

    
class Element(Function):

    def __init__(self, config, inputData, returnPipe):
        super().__init__(config, inputData, returnPipe)


    def execute(self):

        n_cnt = 5
        while n_cnt > 0:
            time.sleep(1)
            n_cnt -= 1
            intemediateRecord = Record(False, "DataIntermediate", "Log")
            
            self.returnPipe.send(intemediateRecord)
            logging.debug("Scheduler Called - {}".format(n_cnt))


        recordDone = Record(True, "Data", "LogMessage")
        self.returnPipe.send(recordDone)