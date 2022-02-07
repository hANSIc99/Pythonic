import queue
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pathlib import PosixPath
try:
    from element_types import Record, Function, ProcCMD, GuiCMD, SetPersist, PythonicError
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD, SetPersist, PythonicError

    
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
        chat_ids = SetPersist('chat_ids')
        callback_short_report = '5m'
        self.callback_query_id = None # stre the last chat id which created a query

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
            
            chat_ids.add(update.message.chat_id) 
            # keyboardButton = KeyboardButton(text="Request Report")
            # buttonb = KeyboardButton()
            # keyboard = [[keyboardButton]]
            # reply_markup = ReplyKeyboardMarkup(keyboard)
            data_short_report = '5m'
            report_button = InlineKeyboardButton(
                text='Request Report: 5min', # text that show to user
                callback_data=data_short_report # text that send to bot when user tap button
            )
            reply_markup = InlineKeyboardMarkup([[report_button]])
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Hello, this chat ID is now registered for communication.",
                reply_markup=reply_markup)

        def unknown(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, I didn\'t understand that command.')

        def message(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Message received')
            guitext = GuiCMD('Message received from: {}, MsgId.: {:d}'.format(update.message.from_user.first_name, update.message.message_id))
            self.return_queue.put(guitext)
            record = Record(update.message, 'Message received from: {}, MsgId.: {:d}'.format(update.message.from_user.first_name, update.message.message_id))
            self.return_queue.put(record)

        def callback_query_handler(update, context):

            data = update.callback_query.data
            self.callback_query_id = update.effective_chat.id

            if data == callback_short_report:
                
                context.bot.answer_callback_query(
                    callback_query_id = update.callback_query.id,
                    text = 'Preparing report...'
                )
                

                guitext = GuiCMD('Report request from: {}'.format(update.callback_query.from_user.first_name))
                self.return_queue.put(guitext)
                record = Record(data, 'Report request from: {}'.format(update.callback_query.from_user.first_name))
                self.return_queue.put(record)


        start_handler       = CommandHandler('start', start) # handler for the start command
        message_handler     = MessageHandler(Filters.text &~ Filters.command, message) # only text and not commands
        unknown_cmd_handler = MessageHandler(Filters.command, unknown) 
        callback_handler    = CallbackQueryHandler(callback_query_handler)

        dispatcher.add_handler(start_handler)
        #dispatcher.add_handler(message_handler) # we don't need to process messages
        dispatcher.add_handler(callback_handler)
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

                filename = cmd.data

                if not filename or not isinstance(filename, PosixPath):
                    cmd = None
                    continue
 
                try:
                    with open(filename, 'rb') as freport:
                        try:
                            dispatcher.bot.send_document(
                                chat_id=self.callback_query_id, 
                                document=freport)
                        except Exception as e:
                            self.return_queue.put(Record(PythonicError(e), 'Error sending message'))

                except OSError as e:
                    self.return_queue.put(Record(PythonicError(e), 'Error opening report'))
 
            cmd = None