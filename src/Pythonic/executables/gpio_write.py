import time, queue
try:
    from element_types import Record, Function, ProcCMD, GuiCMD, PythonicError
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD, PythonicError
    
from gpiozero import LED, PWMLED

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
        subModeLED      = None
        subModePWMLED   = None
        gpioWorker      = None
        cmd             = None

        self.gpio       = None
        self.initFlag   = False

        for attrs in specificConfig:
            if attrs['Name'] == 'GPIO':
                gpioName = attrs['Data']
            if attrs['Name'] == 'MainMode':
                mainMode = attrs['Data']
            elif attrs['Name'] == 'SubModeLED':
                subModeLED = attrs['Data']
            elif attrs['Name'] == 'SubModePWMLED':
                subModePWMLED = attrs['Data']




        if mainMode == 'LED':

            self.gpio = LED(gpioName, initial_value=False)

            if subModeLED == 'Toggle on input':

                gpioWorker = self.ledWorkerToggle
                self.gpio.toggle()
                self.logLEDstate()

            elif subModeLED == 'Control on Input':

                gpioWorker = self.ledWorkerCtrl
                # set initial state
                if self.inputData is not None:
                    if self.inputData:
                        self.gpio.on()
                    else:
                        self.gpio.off()

                    self.logLEDstate()

            elif subModeLED == 'Blink':
                def a(cmd = None): pass
                gpioWorker = a # assign an empty function
                self.gpio.blink()
                self.return_queue.put(Record(None, 'Start LED Blink Mode on GPIO{}'.format(self.gpio.pin.number))) 



        elif mainMode == 'PWMLED': 

            self.gpio = PWMLED(gpioName, initial_value=False)

            if subModePWMLED == 'Control on Input':

                gpioWorker = self.pwmLedWorkerCtrl

                if self.inputData is not None:
                    self.gpio.value = self.inputData
                    self.return_queue.put(Record(None, 'PWMLED: Set brightness on GPIO{} to {:.2f}'.format(self.gpio.pin.number, self.inputData))) 

            elif subModePWMLED == 'Pulse':
                def a(cmd = None): pass
                gpioWorker = a # assign an empty function
                self.gpio.pulse()
                self.return_queue.put(Record(None, 'Start PWMLED Pulse Mode on GPIO{}'.format(self.gpio.pin.number))) 

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

            gpioWorker(cmd)

    def logLEDstate(self):   
        self.return_queue.put(Record(None, 'Switch LED on GPIO{} to {}'.format(self.gpio.pin.number, self.gpio.is_active))) 

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

    def pwmLedWorkerCtrl(self, cmd = None):

        if cmd is None:
            return
        try:
            self.gpio.value = cmd.data
        except Exception:
            self.gpio.close()
            raise
        self.return_queue.put(Record(None, 'PWMLED: Set brightness on GPIO{} to {:.2f}'.format(self.gpio.pin.number, cmd.data)) ) 