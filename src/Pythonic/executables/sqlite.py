import time, queue, sqlite3
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

        specificConfig = self.config.get('SpecificConfig')

        if not specificConfig:

            recordDone = Record(None, message='Config missing')
            self.return_queue.put(recordDone)
            return

        filename = None

        for attrs in specificConfig:
            if attrs['Name'] == 'Filename':
                filename = attrs['Data']

        con = sqlite3.connect(filename)
        # TODO 
        if not con:
            raise Exception('Can not connect to database')

        if self.inputData is None:
            output = 0
        else:
            output = self.inputData + 1


        
        #########################################
        #                                       #
        #    The execution exits immediately    #
        #    after providing output data        #
        #                                       #
        #########################################

        recordDone = Record(output, 'Sending value of cnt: {}'.format(output))     
        self.return_queue.put(recordDone)