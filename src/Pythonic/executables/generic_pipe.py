import time, queue
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD
    
class Element(Function):

    def __init__(self, config, inputData, return_queue, cmd_queue):
        super().__init__(config, inputData, return_queue, cmd_queue)


    def execute(self):


        #####################################
        #                                   #
        #     REFERENCE IMPLEMENTATION      #
        #                                   #
        #####################################



        output = input + 1


        
        #########################################
        #                                       #
        #    The execution exits immediately    #
        #    after providing output data        #
        #                                       #
        #########################################

        recordDone = Record(output, 'Sending value of cnt: {}'.format(output))     
        self.return_queue.put(recordDone)