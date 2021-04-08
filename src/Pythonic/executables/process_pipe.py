import time, queue
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD
    
class Element(Function):

    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        super().__init__(id, config, inputData, return_queue, cmd_queue)


    def execute(self):


        #####################################
        #                                   #
        #     REFERENCE IMPLEMENTATION      #
        #                                   #
        #####################################


        cmd = None
        cnt = 0

        #####################################
        #                                   #
        #     Start of the infinite loop    #
        #                                   #
        #####################################

        # The example executes an infinite loop till it's receives a stop command
        while(True):

            # Example code: Do something

            try:
                # Block for 1 second and wait for incoming commands 
                cmd = self.cmd_queue.get(block=True, timeout=1)
            except queue.Empty:
                pass

            if isinstance(cmd, ProcCMD):
                if cmd.bStop:
                    # Stop command received, exit
                    return
                else:
                    # Example Code: Send number of received data packets to GUI
                    cnt+=1
                    guitext = GuiCMD('Data received: {}'.format(cnt))
                    self.return_queue.put(guitext)
                    cmd.data += 1
                    
                    # Example Code: Increment received data by one and forward it to subsequent elements
                    recordDone = Record(cmd.data, 'Sending value of cnt: {}'.format(cmd.data))     
                    self.return_queue.put(recordDone)
                    
                    cmd = None




