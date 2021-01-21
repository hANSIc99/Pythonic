from Pythonic.record_function import Record, Function
from email.message import EmailMessage
from sys import getsizeof
import smtplib, ssl, pickle

class ConnMailFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        #logging.debug('ConnMailFunction::__init__() called')

    def execute(self, record):

        # recipient, sender, password, server_url, server_port, subject
        # input_opt_index, input_opt_data, filename, pass_input, message_state, message_txt, log_state

        recipient, sender, password, server_url, server_port, subject, \
                input_opt_index, input_opt_data, filename, pass_input, message_state, \
                message_txt, log_state = self.config

        if input_opt_index == 1: # Use input as message txt
            if message_state: # In case there is already a message, append input
                message_txt += '\n\n'
                message_txt += str(record)
            else:
                message_state = True
                message_txt = str(record)


        if isinstance(record, dict): # Dictionary has always priority
                if 'subject' in record: 
                    subject = record['subject']
                if 'message' in record: 
                    message_state = True
                    message_txt = record['message']

        rcp_list = recipient.split(' ')

        # Message constructor
        msg = EmailMessage()
        msg['Subject']  = subject
        msg['From']     = sender
        msg['To'] = ', '.join(rcp_list)
        msg.set_default_type('text/plain')
        if message_state:
            msg.set_content(message_txt)

        # Attachment

        if input_opt_index == 2: # Attach input object as string
            if not filename:
                filename = 'filename.txt'
            msg.add_attachment(str(record), 'text/plain', filename=filename)

        if input_opt_index == 3: # Attach input object as binary
            attachement = pickle.dumps(record)
            if not filename:
                filename = 'filename.txt'
            msg.add_attachment(attachement, maintype='application', subtype='octet-stream',
                    filename='filename.bin')

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(server_url, server_port, context=context) as server:
            server.login(sender, password)
            server.send_message(msg)
        
        if not pass_input:
            record = None

        log_txt = '{{SEND MAIL}}              {} bytes send'.format(getsizeof(msg.__str__()))

        result = Record(self.getPos(), (self.row +1, self.column), record, log=log_state, log_txt=log_txt)

        return result
