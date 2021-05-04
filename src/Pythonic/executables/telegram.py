import logging, queue
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

try:
    from element_types import Record, Function, ProcCMD, GuiCMD, ListPersist
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD, ListPersist

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

        cmd = None
        specificConfig = self.config.get('SpecificConfig')
        chat_ids = ListPersist('chat_ids')

        if not specificConfig:

            recordDone = Record(None, message='Config missing')
            self.return_queue.put(recordDone)
            return


        token = next(attr['Data'] for attr in specificConfig if attr['Name'] == 'Token')

        if not token:
            recordDone = Record(None, message='Token missing')
            self.return_queue.put(recordDone)
            return

        updater = Updater(token=self.config['SpecificConfig'][0]['Data'], use_context=True)

        dispatcher = updater.dispatcher


        def start(update: Update, context: CallbackContext):
            
            chat_ids.append(update.message.chat_id) 
            context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, this chat ID is now registered for communication.")


        def unknown(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, I didn\'t understand that command.')

        def message(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Message received')
            guitext = GuiCMD('Message received from: {}, MsgId.: {:d}'.format(update.message.from_user.first_name, update.message.message_id))
            self.return_queue.put(guitext)
            record = Record(update.message, 'Message received from: {}, MsgId.: {:d}'.format(update.message.from_user.first_name, update.message.message_id))
            self.return_queue.put(record)

        start_handler       = CommandHandler('start', start)
        message_handler     = MessageHandler(Filters.text &~ Filters.command, message)
        unknown_cmd_handler = MessageHandler(Filters.command, unknown)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(message_handler) # muss als letztes hinzugefügt werden
        dispatcher.add_handler(unknown_cmd_handler)

        updater.start_polling()

        while(updater.running):

            try:
                # Block for 1 second and wait for incoming commands 
                cmd = self.cmd_queue.get(block=True, timeout=1)
            except queue.Empty:
                pass

            if isinstance(cmd, ProcCMD) and cmd.bStop:
                # Stop command received, exit
                updater.stop()

            elif isinstance(cmd, ProcCMD):

                guitext = GuiCMD("Sending data: " + str(cmd.data))
                self.return_queue.put(guitext)

                for chat_id in chat_ids:
                    try:
                        dispatcher.bot.send_message(chat_id=chat_id, text=str(cmd.data))
                    except Exception as e:
                        logging.error(e)
                        chat_ids.remove(chat_id)
                        logging.warning('ChatId removed')
                    


            cmd = None

