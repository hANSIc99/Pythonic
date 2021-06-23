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

            self.gpio = LED(gpioName, initial_value=False)

            if subMode == 'Toggle on input':

                gpioWorker = self.ledWorkerToggle
                self.gpio.toggle()
                self.logLEDstate()

            elif subMode == 'Control on Input':

                gpioWorker = self.ledWorkerCtrl
                # set initial state
                if self.inputData is not None:
                    if self.inputData:
                        self.gpio.on()
                    else:
                        self.gpio.off()

                    self.logLEDstate()

            elif subMode == 'Blink':
                def a(cmd = None): pass
                gpioWorker = a # assign an empty function
                self.gpio.blink()
                recordDone = Record(None, 'Start LED Blink Mode on GPIO{}'.format(self.gpio.pin.number))     
                self.return_queue.put(recordDone) 
        

        # The example executes an infinite loop till it's receives a stop command
        while(True):

            # Example code: Do something

            try:
                # Block for 1 second and wait for incoming commands 
                cmd = None
                cmd = self.cmd_queue.get(block=True, timeout=1)
            except queue.Empty:
                pass

            if isinstance(cmd, ProcCMD):
                if cmd.bStop:
                    # Stop command received, exit
                    recordDone = Record(None, 'GPIO{} closed'.format(self.gpio.pin.number))     
                    self.return_queue.put(recordDone) 
                    self.gpio.close()
                    return

            gpioWorker(cmd)

    def logLEDstate(self):
        recordDone = Record(None, 'Switch LED on GPIO{} to {}'.format(self.gpio.pin.number, self.gpio.is_active))     
        self.return_queue.put(recordDone) 

    def ledWorkerToggle(self, cmd = None):

        if cmd is None:
            return

        self.gpio.toggle()
        self.logLEDstate()


    def ledWorkerCtrl(self, cmd = None):

        if cmd is None:
            return

        if cmd.data:
            self.gpio.on()
        else:
            self.gpio.off()

        self.logLEDstate()

