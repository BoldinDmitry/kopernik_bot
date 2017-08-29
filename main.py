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
root_menu_flag = {}
adding_question = []
buttons_last_root = {}
for_adding_root = {}


@bot.message_handler(func=lambda message: message.text in [strings["menu"]["menu_name"], "/start"])
def send_welcome(message):
    """
    Функция, показывающая reply_markup с кнопками меню
    :param message: Сообщение, присланное пользователем
    """

    botan.track(botan_key, message.chat.id, message.text, strings["menu"]["menu_name"])

    global faq_flag

    if message.chat.id in faq_flag:
        del faq_flag[message.chat.id]

    markup = types.ReplyKeyboardMarkup()
    for button in strings["menu"]["keyboard_buttons"]:
        markup.add(button)

    bot.send_message(message.chat.id, strings["menu"]["message"], reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == strings["faq"]["call_mes"] or message.chat.id in faq_flag)
def faq(message):
    global buttons_last, faq_flag, buttons_now

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
            send_welcome(message)
            return None
    else:
        buttons_last[message.chat.id].append(message.text)

    try:
        buttons_now = tree_parser(buttons_last[message.chat.id])
    except KeyError:
        bot.send_message(message.chat.id, "Выбирите, пожалуйста, одну из категорий вопросов")
        return

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


@bot.message_handler(func=lambda message: message.text.lower() == strings["root_menu"]["menu_name"] and
                                          message.chat.id in strings["admin_id"])
def root_menu(message):
    global root_menu_flag

    markup = types.ReplyKeyboardMarkup()

    root_menu_flag[message.chat.id] = strings["root_menu"]["menu_name"]

    for button in strings["root_menu"]["keyboard_buttons"]:
        markup.add(button)

    bot.send_message(message.chat.id, strings["root_menu"]["message"], reply_markup=markup)


@bot.message_handler(func=lambda message: strings["add_question"]["call_mes"] == message.text and
                                          strings["root_menu"]["menu_name"] == root_menu_flag.get(message.chat.id) or
                                          strings["add_question"]["call_mes"] == root_menu_flag.get(message.chat.id))
def add_question_root(message):
    global buttons_last_root, root_menu_flag, for_adding_root

    root_menu_flag[message.chat.id] = strings["add_question"]["call_mes"]
    print(buttons_last_root)
    if message.text == strings["add_question"]["call_mes"]:
        buttons_last_root[message.chat.id] = []

    elif len(buttons_last_root[message.chat.id]) > 0:
        if message.text == strings["add_question"]["add_here"]:
            bot.send_message(message.chat.id, strings["add_question"]["ask_about_question"])

            buttons_last_root[message.chat.id].append(strings["add_question"]["ask_about_question"])
            return

        if buttons_last_root[message.chat.id][-1] == strings["add_question"]["ask_about_question"]:
            for_adding_root[message.chat.id] = {"question": message.text}

            bot.send_message(message.chat.id, strings["add_question"]["ask_about_answer"])
            buttons_last_root[message.chat.id] \
                .append(strings["add_question"]["ask_about_answer"])
            return
        if buttons_last_root[message.chat.id][-1] == strings["add_question"]["ask_about_answer"]:
            for_adding_root[message.chat.id]["answer"] = message.text
            print(buttons_last_root[message.chat.id])
            print(for_adding_root[message.chat.id]["question"])
            print(for_adding_root[message.chat.id]["answer"])
            print(buttons_last_root)
            add_question(buttons_last_root[message.chat.id][:-2], for_adding_root[message.chat.id]["question"],
                         for_adding_root[message.chat.id]["answer"])
            return
    else:
        buttons_last_root[message.chat.id].append(message.text)

    buttons_now_root = tree_parser(buttons_last_root[message.chat.id])

    markup = types.ReplyKeyboardMarkup()

    for button in buttons_now_root:
        markup.add(button)
    markup.add(strings["add_question"]["add_here"])
    bot.send_message(message.chat.id, strings["add_question"]["message"], reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
