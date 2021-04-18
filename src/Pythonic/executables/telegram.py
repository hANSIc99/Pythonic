import time, queue
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import InlineQueryHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)


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

        def start(update, context):
            location_keyboard = KeyboardButton(text="send_location", request_location=True)
            #custom_keyboard = [[ location_keyboard ]]
            #reply_markup = ReplyKeyboardMarkup(custom_keyboard)
            #context.bot.send_message(chat_id=update.effective_chat.id, 
            #                text="Would you mind sharing your location and contact with me?", 
            #                reply_markup=reply_markup)
            context.bot.send_message(chat_id=update.effective_chat.id, 
                            text="Hello from bot")


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

        while(updater.running):

            try:
                # Block for 1 second and wait for incoming commands 
                cmd = self.cmd_queue.get(block=True, timeout=1)
            except queue.Empty:
                pass

            if isinstance(cmd, ProcCMD) and cmd.bStop:
                # Stop command received, exit
                updater.stop()