# -*- coding: utf-8 -*-
import configparser
from telegram.ext import Updater
import logging
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

config=configparser.ConfigParser()
config.read("config.ini")
bot_token = config["DEFAULT"]["token"]
REQUEST_KWARGS={}
if config.has_option("DEFAULT","proxy_url")==True:
    REQUEST_KWARGS={"proxy_url": config["DEFAULT"]["proxy_url"]} 

hi_txt="Hi {username}. My name is {bot_name}.\nI'm echo bot"

updater = Updater(token=bot_token, request_kwargs = REQUEST_KWARGS)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    start_txt=hi_txt
    start_msg=start_txt.format(username=update.message.from_user.first_name, bot_name=bot.name)
    bot.send_message(chat_id=update.message.chat_id, text=start_msg)

def echo(bot, update):
    update.message.reply_text(update.message.text)

def main():
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
