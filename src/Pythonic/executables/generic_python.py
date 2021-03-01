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


        # Use this example method for 



        cmd = None
        cnt = 0

        

        # To exit immediately after providing output data, uncomment this

        #recordDone = Record(cnt, 'Sending value of cnt: {}'.format(cnt))     
        #self.queue.put(recordDone)
        #return

        # The example executes an infinite loop till it's receives a stop command
        while(True):

            cnt+=1

            try:
                # Block for 1 second and wait for incoming commands 
                cmd = self.cmd_queue.get(block=True, timeout=1)
            except queue.Empty:
                pass

            if isinstance(cmd, ProcCMD) and cmd.bStop:
                # Stop command received, exit
                return



            # Send status text to GUI every timeout interval
            guitext = GuiCMD('cnt: {}'.format(cnt))
            self.return_queue.put(guitext)


            # Send data to element output every 5 x timeout
            if cnt % 5 == 0:
                # Recors(data, message)
                recordDone = Record(cnt, 'Sending value of cnt: {}'.format(cnt))     
                self.return_queue.put(recordDone)




