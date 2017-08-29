import telebot
import config
import botan

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


def main_menu(message):
    """
    Функция, показывающая reply_markup с кнопками меню
    :param message: Сообщение, присланное пользователем
    """

    botan.track(botan_key, message.chat.id, message.text, strings["menu"]["menu_name"])

    global faq_flag
    if message.chat.id in faq_flag:
        faq_flag.remove(message.chat.id)
    markup = types.ReplyKeyboardMarkup()
    for button in strings["menu"]["keyboard_buttons"]:
        markup.add(button)
    bot.send_message(message.chat.id, strings["menu"]["message"], reply_markup=markup)


def faq_menu(message):
    global buttons_last
    global faq_flag
    global buttons_now

    botan.track(botan_key, message.chat.id, message.text, strings["faq"]["call_mes"])

    if message.text == strings["faq"]["call_mes"]:
        buttons_last[message.chat.id] = []
        faq_flag.append(message.chat.id)
    elif message.text == strings["back_button"]:
        if len(buttons_last[message.chat.id]) > 0:
            buttons_last[message.chat.id].pop()
        else:
            del buttons_last[message.chat.id]
            del faq_flag[message.chat.id]
            send_main_menu(message)
            return None
    else:
        buttons_last[message.chat.id].append(message.text)
    try:
        buttons_now = tree_parser(buttons_last[message.chat.id])
    except KeyError:
        bot.send_message(message.chat.id, "Выбирите, пожалуйста, одну из категорий вопросов")
        return None
    if type(buttons_now) is str:
        markup = types.ReplyKeyboardMarkup()
        markup.add(strings["menu"]["menu_name"])
        markup.add(strings["call_admin"])
        markup.add(strings["back_button"])
        bot.send_message(message.chat.id, buttons_now, reply_markup=markup)

    elif type(buttons_now) is dict:
        bot.send_message(message.chat.id, "Тогда напиши админу:")
        markup = types.ReplyKeyboardMarkup()
        markup.add(strings["menu"]["menu_name"])
        bot.send_contact(message.chat.id, phone_number=buttons_now["phone_number"],
                         first_name=buttons_now["first_name"], reply_markup=markup)

        botan.track(botan_key, message.chat.id, message.text, strings["call_admin"])

    else:

        buttons_now.append(strings["call_admin"])
        buttons_now.append(strings["back_button"])
        markup = types.ReplyKeyboardMarkup()
        for button in buttons_now:
            markup.add(button)

        bot.send_message(message.chat.id, strings["faq"]["message"], reply_markup=markup)
