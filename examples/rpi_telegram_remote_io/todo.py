import sys
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)

    if content_type == 'text':
        if msg['text'] == '/key':
            bot.sendMessage(chat_id, 'testing custom keyboard',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
                                ]
                            ))


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
print('Listening ...')
bot.message_loop({'chat': on_chat_message}, run_forever=True)
