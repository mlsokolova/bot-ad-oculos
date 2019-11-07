# -*- coding: utf-8 -*-
import configparser
from telegram.ext import Updater
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram.ext import CommandHandler
from telegram import ParseMode
from enrich_phrase import get_enrich_phrase
import wikidata as wd
import args_handler


config=configparser.ConfigParser()
config.read("config.ini")
bot_token = config["DEFAULT"]["token"]
REQUEST_KWARGS={}
if config.has_option("DEFAULT","proxy_url")==True:
    REQUEST_KWARGS={"proxy_url": config["DEFAULT"]["proxy_url"]} 

start_message="Organic self-educated bot"
hi_txt="Hi {username}. My name is {bot_name}.\n"

commands_txt = "I can understand the following commands:\n"
commands_txt  += "/info - information about me\n"
#commands_txt += "/go - let's go with the keyboard buttons\n"
commands_txt += "/ru_swear <phrase> - enrich you phrase with the russian swear words. Try: /ru_swear Привет, чудесный день сегодня! Как дела? \n" 
commands_txt += "/wikidata search=<Concept, Name, etc> lang=<language>  - query on wikidata.org. Try: /wikidata search=Telegram lang=en"
info_txt = "I live in the CentOS docker container and working through the Tor socket.\n"
info_txt += "Docker container placed on the VirtualBox machine.\n"
info_txt += "VirtualBox machine placed on the Linux Fedora comp.\n"
#info_txt += "Looks like a Death of Кощей Бессмертный, isn't it?\n"

ru_swear_rezult_txt = u"{username}, enriched phrase would be the following:\n\n{phrase}"

under_construction_txt = "In this part, I'm under construction"

updater = Updater(token=bot_token, request_kwargs = REQUEST_KWARGS)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    start_txt=hi_txt+commands_txt
    start_msg=start_txt.format(username=update.message.from_user.first_name, bot_name=bot.name)
    bot.send_message(chat_id=update.message.chat_id, text=start_msg)

def info(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=info_txt + "\n" + commands_txt.format(username=""))

def go(bot, update):
    reply_buttons = [[InlineKeyboardButton("BI Technologies", callback_data="bi_tech"),InlineKeyboardButton("Russian Swear Words", callback_data="ru_swear")]]
    inline_buttons = [[InlineKeyboardButton("BI Technologies", callback_data="bi_tech"),InlineKeyboardButton("Russian Swear Words", callback_data="/ru_swear")]]
#    reply_keyboard = ReplyKeyboardMarkup(reply_buttons)
    inline_keyboad = InlineKeyboardMarkup(inline_buttons)
    update.message.reply_text("Please choose", reply_markup=inline_keyboad)
#    update.message.reply_text(", push the button", reply_markup=reply_keyboard)


def ru_swear(bot, update, args):
    #print("args = " + " ".join(args))
    #print(args)
    phrase = " ".join(args)
    #print phrase
    #filename = "swear.txt"
    enriched_phrase = get_enrich_phrase(phrase)
    update.message.reply_text(ru_swear_rezult_txt.format(username=update.message.from_user.first_name,phrase=enriched_phrase))
    #update.message.reply_text(enriched_phrase)

def button(bot,update):
    topic=""
    query = update.callback_query
    topic=query.data
    if topic=="bi_tech": 
        query.edit_message_text(text=under_construction_txt)    
    elif topic=="ru_swear": 
        #ru_swear_handler = MessageHandler(Filters.text, ru_swear)
        #dispatcher.add_handler(ru_swear_handler)       
        query.edit_message_text(text=under_construction_txt)

def wikidata(bot,update,args):
    #print(args)
    args_string = " ".join(args)
    #print(args_string)
    wikidata_valid_args_list = ["search=","lang="]
    status, result = args_handler.parameters_handler(args_string=args_string, valid_args_list=wikidata_valid_args_list)
    if (status==0): 
        search = result.get("search=")
        lang = result.get("lang=")
        #wd.get_qualifiers_count_by_label_and_language("Oracle", "en")
        #print "search=" + search +" lang=" + lang
        query_count=wd.get_qualifiers_count_by_label_and_language(label_value=search, language=lang)
        update.message.reply_text(query_count)
        query_result_table = wd.get_qualifiers_by_label_and_language(label_value=search, language=lang)
        update.message.reply_text( query_result_table, parse_mode="html")

    elif (status==1):
        update.message.reply_text(result.format(c=" /wikidata "))


def main():
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", info)
    info_handler = CommandHandler("info", info)
    go_handler = CommandHandler("go", go)
    button_handler = CallbackQueryHandler(button)
    ru_swear_handler = CommandHandler("ru_swear", ru_swear, pass_args=True)
    wikidata_handler = CommandHandler("wikidata", wikidata, pass_args=True)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(go_handler)
    dispatcher.add_handler(button_handler)
    dispatcher.add_handler(ru_swear_handler)
    dispatcher.add_handler(wikidata_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
