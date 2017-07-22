import json


with open("json_files/tree.json") as json_file:
    tree = json.load(json_file)


def tree_parser(buttons_names: list) -> list:
    if not buttons_names:
        return list(tree.keys())
    else:
        new_tree = tree
        for button in buttons_names:
            new_tree = new_tree[button]

        if type(new_tree) is str:
            return new_tree
        elif "phone_number" in list(new_tree.keys()):
            return new_tree
        else:
            return list(new_tree.keys())


def add_question(buttons_names: list, question: str, answer: str):
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
