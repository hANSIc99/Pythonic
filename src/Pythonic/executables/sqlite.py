import time, queue, sqlite3
try:
    from element_types import Record, Function, ProcCMD, GuiCMD, PythonicError
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
        output = None

        for attrs in specificConfig:
            if attrs['Name'] == 'Filename':
                filename = attrs['Data']

        if self.inputData is None:
            recordDone = Record(None, message='No input provided')
            self.return_queue.put(recordDone)
            return

        con = sqlite3.connect(filename)

        if not con:
            raise Exception('Can not connect to database')

        cur = con.cursor()

        try:
            cur.execute(self.inputData)
        except Exception as e:
            recordDone = Record(PythonicError(e), 'Query failed') 
            self.return_queue.put(recordDone)
            con.close()    
            return

        output = cur.fetchall()

        con.commit()
        con.close()
        recordDone = Record(output, 'Query successful')     
        self.return_queue.put(recordDone)