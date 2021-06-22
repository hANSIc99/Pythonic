import time, queue
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD
    
from gpiozero import LED

class Element(Function):

    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        super().__init__(id, config, inputData, return_queue, cmd_queue)


    def execute(self):

        #####################################
        #                                   #
        #     REFERENCE IMPLEMENTATION      #
        #                                   #
        #####################################
        specificConfig = self.config.get('SpecificConfig')

        if not specificConfig:

            recordDone = Record(None, message='Trigger: {:04d}'.format(self.config['Identifier']))
            self.return_queue.put(recordDone)
            return

        gpioName   = None
        mainMode   = None
        subMode    = None
        gpioWorker = None
        cmd        = None

        self.gpio       = None
        self.initFlag   = False

        for attrs in specificConfig:
            if attrs['Name'] == 'GPIO':
                gpioName = attrs['Data']
            if attrs['Name'] == 'MainMode':
                mainMode = attrs['Data']
            elif attrs['Name'] == 'SubMode':
                subMode = attrs['Data']




        #####################################
        #                                   #
        #     Start of the infinite loop    #
        #                                   #
        #####################################




        if mainMode == 'LED':

            self.gpio = LED(gpioName)

            if subMode == 'Toggle on input':

                gpioWorker = self.ledWorkerToggle

            elif subMode == 'Control on Input':

                gpioWorker = self.ledWorkerCtrl

            elif subMode == 'Blink':
                gpioWorker = self.ledWorkerBlink
        


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
                    self.gpio.close()
                    return
                else:
                    # Example Code: Send number of received data packets to GUI

                    #if sub_mode

                    #guitext = GuiCMD('Data received: {}'.format(str(cmd)))
                    #self.return_queue.put(guitext)

                    
                    # Send only a message
                    recordDone = Record(None, 'Command received')     
                    self.return_queue.put(recordDone)
                    
                    cmd = None


            gpioWorker(cmd)


    def ledWorkerToggle(self, cmd = None):
        return

    def ledWorkerCtrl(self, cmd = None):

        if cmd is None:
            return

        if cmd.data:
            self.gpio.on()
        else:
            self.gpio.off()

    def ledWorkerBlink(self, cmd = None):
        
        if not self.initFlag:
            self.initFlag = True
            self.gpio.blink()


