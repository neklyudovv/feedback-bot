import os
from telegram import Update
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, CommandHandler


def admin_handler(update: Update, context: CallbackContext):  # admin: отвечать на сообщения чтобы бот пересылал ответ юзеру
    #update.message.reply_text(text='adm')
    if update.message.reply_to_message:
        user = update.message.from_user
        msg_text = update.message.reply_to_message['text']
        msg_text = msg_text[msg_text.find(':')+1:]
        id = msg_text[:msg_text.find(':')]
        text = f'{user["username"]} Ответил вам: \n{update.message.text}'
        context.bot.sendMessage(chat_id=id, text=text)


def regular_handler(update: Update, context: CallbackContext):  # user: /start, написать сообщение которое будет форснуто админу
    user = update.message.from_user
    text = f'@{user["username"]}:{user["id"]}: пишет:\n{update.message.text}'
    context.bot.sendMessage(chat_id=1046754707, text=text)


def message_handler(update: Update, context: CallbackContext):
    user = update.message.from_user
    if user['id'] == 1046754707: # if user == admin
        admin_handler(update, context)
    else:
        regular_handler(update, context)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(text='Привет, можешь написать все что хочешь')
    # context.bot.send_message(chat_id=update.effective_chat.id, text="start")


def main():
    updater = Updater(token=os.environ['TOKEN'], use_context=True)
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)  # start handler
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))  # all messages handler
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
