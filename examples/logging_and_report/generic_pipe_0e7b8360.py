import time, queue, logging, os
from random import randrange
try:
    from element_types import Record, Function, ProcCMD, GuiCMD, PythonicError
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD, PythonicError
    
class Element(Function):

    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        super().__init__(id, config, inputData, return_queue, cmd_queue)


    def execute(self):

        # Raspberry Pi only
        #cpu_temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "").replace("'C\n", "")
        #cpu_temp = float(cpu_temp)

        # Generate random temperature
        cpu_temp = randrange(450, 500)
        cpu_temp = float(cpu_temp/10)

        output = 'INSERT INTO my_table VALUES ({}, {})'.format(int(time.time()), cpu_temp)
        
        recordDone = Record(output)     
        self.return_queue.put(recordDone)