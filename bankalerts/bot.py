from telegram.ext import *

updater = Updater(token='5309472147:AAELS5dCEgXUsRLKGfUyEj27qRX9hyU1kI4', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def start_command(update, context):
    update.message.reply_text('enter your email')


start_handler = CommandHandler('start', start_command)
dispatcher.add_handler(start_handler)
updater.start_polling()
updater.idle()
