import time, queue
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import InlineQueryHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)



from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

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

            context.bot.send_message(chat_id=update.effective_chat.id, text="Hello from bot")


        def echo(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

        def caps(update, context):
            text_caps = ''.join(context.args).upper()
            context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

        def inline_caps(update, context):
            query = update.inline_query.query
            if not query:
                return
            results = list()
            results.append(
                    InlineQueryResultArticle(
                        id=query.upper(),
                        title='Caps',
                        input_message_content=InputTextMessageContent(query.upper())
                    )
            )
            context.bot.answer_inline_query(update.inline_query.id, results)

        inline_caps_handler = InlineQueryHandler(inline_caps)

        def unknown(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, I didn\'t understand that command.')

        def send_message(context: CallbackContext, text):
            """Send the alarm message."""
            job = context.job
            context.bot.send_message(job.context, text='Beep!')


        start_handler = CommandHandler('start', start)
        echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
        caps_handler = CommandHandler('caps', caps)
        unknown_handler = MessageHandler(Filters.command, unknown)
        #echo_handler = MessageHandler(Filters.location & (~Filters.command), echo)

        dispatcher.add_handler(start_handler)
        #dispatcher.add_handler(echo_handler)
        #dispatcher.add_handler(caps_handler)
        dispatcher.add_handler(inline_caps_handler)
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
                #try:
                 #dispatcher.job_queue.run_once(lambda context: context.bot.send_message(context.job.context, text='test123', ), 0)
                dispatcher.job_queue.run_once(send_message, 0, job_kwargs={ 'kwargs' : {'text' : 'Hello From Pythonic'}})
                #except Exception as e:
                #    errorRecord = Record(None, 'Telegram Exception: {}'.format(str(e)))     
                #    self.return_queue.put(errorRecord)

            cmd = None

