import telebot
from telebot import types

import config
from faq import *
from text_files.strings import *

bot = telebot.TeleBot(config.key)

buttons_last = {}
faq_flag = []
buttons_now = {}
confirming = []
root_menu_flag = []
adding_question = []


@bot.message_handler(func=lambda message: message.text in [strings["menu"]["menu_name"], "/start"])
def send_welcome(message):
    global faq_flag
    if message.chat.id in faq_flag:
        faq_flag.remove(message.chat.id)
    markup = types.ReplyKeyboardMarkup()
    for button in strings["menu"]["keyboard_buttons"]:
        markup.add(button)
    bot.send_message(message.chat.id, strings["menu"]["message"], reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == strings["faq"]["call_mes"] or message.chat.id in faq_flag)
def faq(message):
    global buttons_last
    global faq_flag
    global buttons_now

    if message.text == strings["faq"]["call_mes"]:
        buttons_last[message.chat.id] = []
        faq_flag.append(message.chat.id)
    elif message.text == strings["back_button"]:
        if len(buttons_last[message.chat.id]) > 0:
            buttons_last[message.chat.id].pop()
        else:
            del buttons_last[message.chat.id]
            faq_flag.remove(message.chat.id)
            send_welcome(message)
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

    else:

        buttons_now.append(strings["call_admin"])
        buttons_now.append(strings["back_button"])
        markup = types.ReplyKeyboardMarkup()
        for button in buttons_now:
            markup.add(button)

        bot.send_message(message.chat.id, strings["faq"]["message"], reply_markup=markup)



if __name__ == '__main__':
    bot.polling(none_stop=True)
