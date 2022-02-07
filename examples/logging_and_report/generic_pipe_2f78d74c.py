import time, queue
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD
    
class Element(Function):

    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        super().__init__(id, config, inputData, return_queue, cmd_queue)


    def execute(self):

        output = None

        # only create a output if a report request was received
        # if a PythonicError type is received do nothing

        if self.inputData == '5m':
            t0 = int(time.time()) # get current unix time
            t1 = t0 - (60 * 5) # calculate unix stamp time 5 minutes ago

            output = 'SELECT * FROM my_table WHERE timestamp BETWEEN {} AND {}'.format(t1, t0)

            recordDone = Record(output)     
            self.return_queue.put(recordDone)