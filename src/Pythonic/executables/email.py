import time, queue, pickle, ssl, smtplib
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
        port        = None
        
        recipients  = None
        subject     = None
        message     = None

        attachments = None


        for attrs in specificConfig:
            if attrs['Name'] == 'Sender':
                sender = attrs['Data']
            elif attrs['Name'] == 'Password':
                password = attrs['Data']
            elif attrs['Name'] == 'URL':
                url = attrs['Data']
            elif attrs['Name'] == 'Port':
                port = int(attrs['Data'])

        if not sender:
            raise Exception('Sender missing in configuration')
        if not password:
            raise Exception('Password missing in configuration')
        if not url:
            raise Exception('URL missing in configuration')
        if not port:
            raise Exception('Port missing in configuration')


        if isinstance(self.inputData, dict):
            if not 'recipient' in self.inputData or not isinstance(self.inputData['recipient'], str):
                recordDone = Record(PythonicError('Key error, see log for details'), message='Key "recipient" not found or not of type string')
                self.return_queue.put(recordDone)
                return
            if not 'subject' in self.inputData or not isinstance(self.inputData['subject'], str):
                recordDone = Record(PythonicError('Key error, see log for details'), message='Key "subject" not found or not of type string')
                self.return_queue.put(recordDone)
                return
            if not 'message' in self.inputData or not isinstance(self.inputData['message'], str):
                recordDone = Record(PythonicError('Key error, see log for details'), message='Key "subject" not found or not of type string')
                self.return_queue.put(recordDone)
                return

            recipients  = self.inputData['recipient']
            subject     = self.inputData['subject']
            message     = self.inputData['message']

            # optional: check for attachment(s)
            if 'attachment' in self.inputData and isinstance(self.inputData['attachment'], list):

                attachments = self.inputData['attachment']

        else:
            recordDone = Record(PythonicError('Config missing'), message='Config missing')
            self.return_queue.put(recordDone)
            return

        msg = EmailMessage()
        msg['Subject']  = subject
        msg['From']     = sender
        msg['To']       = recipients
        msg.set_default_type('text/plain')
        msg.set_content(message)

        if attachments:
            for attachment in attachments:
                if not 'filename' in attachment: # and not isinstance(attachment['filename'], str):
                    continue
                if not isinstance(attachment['filename'], str):
                    continue
                if not 'data' in attachment:
                    continue

                # attach data as text
                if isinstance(attachment['data'], str):
                    msg.add_attachment(attachment['data'], 'text/plain', filename=attachment['filename'])

                else: # attach data is binary object
                    msg.add_attachment(pickle.dumps(attachment['data']), maintype='application', subtype='octet-stream',
                        filename=attachment['filename'])



        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(url, port, context=context) as server:
            server.login(sender, password)
            server.send_message(msg)