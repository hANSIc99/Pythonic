import time, queue
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD
    
from gpiozero import Button

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
            self.return_queue.put(Record(None, message='Trigger: {:04d}'.format(self.config['Identifier'])))
            return

        gpioName        = None
        mainMode        = None
        cmd             = None

        self.gpio       = None
        self.initFlag   = False

        for attrs in specificConfig:
            if attrs['Name'] == 'GPIO':
                gpioName = attrs['Data']
            if attrs['Name'] == 'MainMode':
                mainMode = attrs['Data']


        self.gpio = Button(gpioName)

        if mainMode == 'Fire when released':

            self.gpio.when_released = self.onReleased

        elif mainMode == 'Fire when pressed': 

            self.gpio.when_pressed = self.onPressed



        #####################################
        #                                   #
        #     Start of the infinite loop    #
        #                                   #
        #####################################

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
                    self.return_queue.put(Record(None, 'GPIO{} closed'.format(self.gpio.pin.number))) 
                    self.gpio.close()
                    return


    def onPressed(self):

        self.return_queue.put(Record(None, 'GPIO{} pressed'.format(self.gpio.pin.number))) 

    def onReleased(self):

        self.return_queue.put(Record(None, 'GPIO{} released'.format(self.gpio.pin.number))) 