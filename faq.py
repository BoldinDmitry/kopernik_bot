import json
from text_files.strings import *

with open("json_files/tree.json") as json_file:
    tree = json.load(json_file)


def tree_parser(buttons_names: list) -> list or str or dict:
    """

    :param buttons_names: лист с названиеям нажатых пользователем кнопок
    :return: Лист, когда результатом работы функции будет новое меню из вопросов/категорий вопросов или контакт,
                    строка, когда резьтат работы функции будет сообщение с ответом на вопрос
    """
    if not buttons_names:
        return list(tree.keys())
    elif buttons_names[-1] == strings["call_admin"]:
        return strings["admin_contact"]
    else:
        new_tree = tree
        for button in buttons_names:
            new_tree = new_tree[button]
        if type(new_tree) is str:
            return new_tree
        else:
            return list(new_tree.keys())


def add_question(buttons_names: list, question: str, answer: str) -> None:
    """

    :param buttons_names: лист с названиеям нажатых пользователем кнопок
    :param question: Вопрос, который необходимо добавить
    :param answer: Ответ на вопрос, который необходимо добавить
    :return: None
    """
    global tree

    new_tree = tree
    for button in buttons_names:
        new_tree = new_tree[button]
    new_tree[question] = answer
    for_return = {}
    for i in range(-len(buttons_names), 0):
        if i == 1-len(buttons_names):
            for_return[buttons_names[i]] = new_tree
        else:
            for_return[buttons_names[i]] = tree[buttons_names[i]]
    tree = for_return
    with open("json_files/tree.json", "w") as outfile:
        json.dump(tree, outfile)


def remove_question(buttons_names: list, question: str) -> int:
    """

    :param buttons_names: лист с названиеям нажатых пользователем кнопок
    :param question: Вопрос, который необходимо удалить
    :return: -1 - Вопрос не найден
              0 - Вопрос был удален
    """
    global tree

    new_tree = tree
    for button in buttons_names:
        new_tree = new_tree[button]
    print(new_tree)
    for_return = {}
    if question not in new_tree.keys():
        return -1

    del new_tree[question]

    for i in range(-len(buttons_names), 0):
        if i == 1-len(buttons_names):
            for_return[buttons_names[i]] = new_tree
        else:
            for_return[buttons_names[i]] = tree[buttons_names[i]]
    tree = for_return

    with open("json_files/tree.json", "w") as outfile:
        json.dump(tree, outfile)

    return 0
