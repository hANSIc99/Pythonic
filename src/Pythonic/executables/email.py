import time, queue
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD

from email.message import EmailMessage
    
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
        
        sender      = None
        password    = None
        url         = None
        
        recipient   = None
        subject     = None
        message     = None

        attachment  = None


        for attrs in specificConfig:
            if attrs['Name'] == 'Sender':
                sender = attrs['Data']
            elif attrs['Name'] == 'Password':
                password = attrs['Data']
            elif attrs['Name'] == 'URL':
                url = attrs['Data']

        if isinstance(self.inputData, dict):
            if not 'recipient' in self.inputData or not isinstance(self.inputData['recipient'], str):
                recordDone = Record(None, message='Key "recipient" not found or not of type string')
                self.return_queue.put(recordDone)
                return
            if not 'subject' in self.inputData or not isinstance(self.inputData['subject'], str):
                recordDone = Record(None, message='Key "subject" not found or not of type string')
                self.return_queue.put(recordDone)
                return
            if not 'message' in self.inputData or not isinstance(self.inputData['message'], str):
                recordDone = Record(None, message='Key "subject" not found or not of type string')
                self.return_queue.put(recordDone)
                return

            recipient   = self.inputData['recipient']
            subject     = self.inputData['subject']
            message     = self.inputData['message']

            # optional: check for attachment(s)
            if 'attachment' in self.inputData and isinstance(self.inputData['attachment'], list):

                attachment = self.inputData['attachment']


            #isinstance(tets)

        else:
            recordDone = Record(None, message='Config missing')
            self.return_queue.put(recordDone)
            return


        
        msg = EmailMessage()
        msg['Subject']  = subject
        msg['From']     = sender
        msg['To']       = recipient
        msg.set_default_type('text/plain')
        msg.set_content(message)

        #########################################
        #                                       #
        #    The execution exits immediately    #
        #    after providing output data        #
        #                                       #
        #########################################

        #recordDone = Record(output, 'Sending value of cnt: {}'.format(output))     
        #self.return_queue.put(recordDone)