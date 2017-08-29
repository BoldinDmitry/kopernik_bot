import telebot
import config
import botan
import menues_functions

from telebot import types
from faq import *
from text_files.strings import *

bot = telebot.TeleBot(config.key)
botan_key = config.analytics_key

buttons_last = {}
faq_flag = []
buttons_now = {}
confirming = []
root_menu_flag = []
adding_question = []
users_menu = {}


@bot.message_handler(func=lambda message: message.text in [strings["menu"]["menu_name"], "/start"])
def send_main_menu(message):
    menues_functions.main_menu(message)


@bot.message_handler(func=lambda message: message.text == strings["faq"]["call_mes"] or message.chat.id in faq_flag)
def send_menu_faq(message):
    menues_functions.faq_menu(message)
