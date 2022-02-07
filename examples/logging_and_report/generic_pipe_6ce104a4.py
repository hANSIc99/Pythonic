import time, queue
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD
    
class Element(Function):

    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        super().__init__(id, config, inputData, return_queue, cmd_queue)


    def execute(self):

        output = 'CREATE TABLE IF NOT EXISTS my_table (timestamp INTEGER PRIMARY KEY NOT NULL, value REAL)'
        recordDone = Record(output, 'Creating table')     
        self.return_queue.put(recordDone)