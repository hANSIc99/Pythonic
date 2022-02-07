import time, queue
try:
    from element_types import Record, Function, ProcCMD, GuiCMD, PythonicError
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD, PythonicError
    
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
            cnt+=1

            try:
                # Block for 1 second and wait for incoming commands 
                cmd = self.cmd_queue.get(block=True, timeout=1)
            except queue.Empty:
                pass

            if isinstance(cmd, ProcCMD) and cmd.bStop:
                # Stop command received, exit
                return



            # Example Code: Send status text to GUI every timeout interval
            guitext = GuiCMD('cnt: {}'.format(cnt))
            self.return_queue.put(guitext)


            # Example code: Send data to element output every 5 x timeout
            if cnt % 5 == 0:
                # Recors(data, message)
                recordDone = Record(cnt, 'ID: 0x{:08x} - Sending value of cnt: {}'.format(self.id, cnt))     
                self.return_queue.put(recordDone)




