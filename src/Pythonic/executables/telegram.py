import logging, queue
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

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
        chat_ids = []
        # Set default mode if SpecificConfig is not defined
        # This is the case if the element was created on the working area
        # but the configuration was never opened

        if not specificConfig:

            recordDone = Record(None, message='Config missing')
            self.return_queue.put(recordDone)
            return


        token = next(attr['Data'] for attr in specificConfig if attr['Name'] == 'Token')

        if not token:
            recordDone = Record(None, message='Token missing')
            self.return_queue.put(recordDone)
            return


        updater = Updater(token='1323666957:AAH6rIDQJty0ixLc9fyrLQIohxks_y6wwho', use_context=True)
        dispatcher = updater.dispatcher


        def start(update: Update, context: CallbackContext):
            
            chat_ids.append(update.message.chat_id) 
            context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, this chat ID is now registered for communication.")



        def unknown(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, I didn\'t understand that command.')

        start_handler = CommandHandler('start', start)
        unknown_handler = MessageHandler(Filters.command, unknown)


        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(unknown_handler) # muss als letztes hinzugefügt werden

        updater.start_polling()
        n_cnt = 0
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
                n_cnt += 1
                guitext = GuiCMD("Data received: " + str(cmd.data) + "  " + str(n_cnt))
                self.return_queue.put(guitext)

                for chat_id in chat_ids:
                    try:
                        dispatcher.bot.send_message(chat_id=chat_id, text=str(cmd.data))
                    except Exception as e:
                        logging.error(e)
                        chat_ids.remove(chat_id)
                        logging.warning('ChatId removed')
                    


            cmd = None

