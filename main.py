import json
import telebot
import config

from telebot import types
from strings import *

with open("tree.json") as json_file:
    tree = json.load(json_file)

bot = telebot.TeleBot(config.key)

buttons_last = []
faq_flag = False


def tree_parser(buttons_names):
    if not buttons_names:
        return list(tree.keys())
    else:
        new_tree = tree
        for button in buttons_names:
            new_tree = new_tree[button]
        if type(new_tree) is str:
            return new_tree
        else:
            return list(new_tree.keys())


@bot.message_handler(func=lambda message: message.text in [strings["menu"]["menu_name"], "/start"])
def send_welcome(message):
    global faq_flag

    faq_flag = False
    markup = types.ReplyKeyboardMarkup()
    for button in strings["menu"]["keyboard_buttons"]:
        markup.add(button)
    bot.send_message(message.chat.id, strings["menu"]["message"], reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == strings["faq"]["call_mes"] or faq_flag)
def faq(message):
    global buttons_last
    global faq_flag

    if message.text == strings["faq"]["call_mes"]:
        buttons_last = []
    elif message.text == strings["back_button"]:
        if len(buttons_last) > 0:
            buttons_last.pop()
        else:
            send_welcome(message)
            return None
    else:
        buttons_last.append(message.text)
    buttons_now = tree_parser(buttons_last)

    if type(buttons_now) is str:
        markup = types.ReplyKeyboardMarkup()
        markup.add(strings["menu"]["menu_name"])
        bot.send_message(message.chat.id, buttons_now, reply_markup=markup)
        faq_flag = False

    else:
        buttons_now.append(strings["back_button"])
        markup = types.ReplyKeyboardMarkup()
        for button in buttons_now:
            markup.add(button)
            faq_flag = True
        bot.send_message(message.chat.id, strings["faq"]["message"], reply_markup=markup)

if __name__ == '__main__':
    bot.polling(none_stop=True)
