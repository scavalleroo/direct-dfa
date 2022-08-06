from pythonds.basic.stack import Stack
from termcolor import colored

import const
from dfa_structure.dfa_node import DFANode


def split(word):
    return [char for char in word]


def add_concatenation(infix_expr):
    token_list = split(infix_expr)
    new_infix_expr = []

    for index, token in enumerate(token_list):
        if index > 0 and token not in [')', '*', '|'] and token_list[index - 1] \
                not in ['(', '|']:
            new_infix_expr.append('.')
        new_infix_expr.append(token)

    return "".join(new_infix_expr)


def infix_to_postfix(infix_expr):
    infix_expr = add_concatenation(infix_expr)
    print(f'\nExpression with concatenation\n{infix_expr}')
    op_stack = Stack()
    postfix_list = []
    token_list = split(infix_expr)

    for token in token_list:
        if token not in const.SYMBOLS.keys():
            postfix_list.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            if op_stack.isEmpty():
                print(colored(const.ERRORS[0], 'red'))
                return ""
            topToken = op_stack.pop()
            while topToken != '(':
                postfix_list.append(topToken)
                if op_stack.isEmpty():
                    print(colored(const.ERRORS[0], 'red'))
                    return ""
                topToken = op_stack.pop()
        else:
            while (not op_stack.isEmpty()) and \
                    (const.SYMBOLS[op_stack.peek()] >= const.SYMBOLS[token]):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.isEmpty():
        postfix_list.append(op_stack.pop())
        if postfix_list[-1] == '(':
            print(colored(const.ERRORS[0], 'red'))
            return ""
    return "".join(postfix_list)


def create_tree(postfix_expr):
    op_stack = Stack()
    if len(postfix_expr) > 1:
        for token in postfix_expr:
            if token == '*' and not op_stack.isEmpty():
                root = DFANode(f'{token}')
                root.left = op_stack.pop()
                op_stack.push(root)
            elif len(op_stack.items) >= 2 and token in const.SYMBOLS.keys():
                root = DFANode(f'{token}')
                root.right = op_stack.pop()
                root.left = op_stack.pop()
                op_stack.push(root)
            else:
                op_stack.push(DFANode(f'{token}'))

        while len(op_stack.items) > 1:
            root = op_stack.pop()
            if not root.left:
                root.left = op_stack.pop()
            else:
                root.right = op_stack.pop()
            op_stack.push(root)
    return op_stack


def create_follow_table(root: DFANode) -> dict:
    n_leaf = root.count_leaf()
    follow_table = {}
    for leaf in range(n_leaf):
        follow_table[leaf + 1] = set()
    follow_table = root.follow(follow_table)
    return follow_table


def create_transition_table(root: DFANode, follow_table: dict) -> (set, dict):
    states_id = [1]
    states_set = [root.first()]
    transition_table = dict()
    allowed_chars = sorted(root.get_characters())
    for key in states_id:
        for c in allowed_chars:
            if c != '#':
                nodes = root.find_leaves_by_data_and_ids(
                    data=c, ids=list(states_set[key - 1]))
                if nodes:
                    elements = tuple()
                    for node in nodes:
                        elements += tuple(follow_table[node.id_n])
                    elements = set(elements)
                    found_key = 0
                    for _key in states_id:
                        if states_set[_key - 1] == elements:
                            found_key = _key
                            break

                    if not found_key:
                        found_key = len(states_id) + 1
                        states_id.append(found_key)
                        states_set.append(elements)
                        if found_key not in transition_table:
                            transition_table[found_key] = dict()

                    if key not in transition_table:
                        transition_table[key] = dict()

                    transition_table[key][c] = found_key

    return allowed_chars, dict(sorted(transition_table.items()))


def check_string(
        string: str,
        transition_table: dict,
) -> (int, bool):
    current_state = 1
    for index, c in enumerate(string):
        if c in transition_table[current_state]:
            current_state = transition_table[current_state][c]
        else:
            return index + 1, False
    if current_state == list(transition_table.keys())[-1] or \
            not transition_table[current_state]:
        return 0, True
    return 0, False


def main():
    # expr = "(a|b)*ab#"
    # a|ba*#
    # a|ba*#
    expr = ""
    while not expr or expr[len(expr) - 1] != '#' or '.' in expr:
        if expr:
            if '.' in expr:
                print(colored(const.ERRORS[5], 'red'))
            else:
                print(colored(const.ERRORS[4], 'red'))

        expr = input("Please enter the regular expression."
                     "\nIt must end with the terminator '#' "
                     "and should not contains '.' symbol\n: ")
    print(f"Expression\n{expr}")

    string = input("Please enter the string to check\n: ")

    postfix_expr = infix_to_postfix(expr)

    if not postfix_expr:
        return
    if postfix_expr == '#|':
        print(colored(const.ERRORS[1], 'red'))
        return
    if postfix_expr == '#.':
        print(colored(const.ERRORS[2], 'red'))
        return

    print(f'\nPostfix\n{postfix_expr}')

    root: DFANode = create_tree(postfix_expr).items[0]
    root.set_all_id()

    print("\nTree")
    root.print_tree()
    follow_table = create_follow_table(root=root)

    print(f'\nFollow table\n{follow_table}')
    allowed_chars, transition_table = create_transition_table(
        root=root, follow_table=follow_table)
    print(f"\nTransition table\n{transition_table}")

    print(f'\nString to match: {string}\n')
    index, match = check_string(string, transition_table)
    if match:
        print(colored(
            f"The string '{string}' MATCH the regexp '{expr}'", 'green'))
    else:
        if index:
            print(colored(
                f"MISMATCH in pos '{index}': '{string[0:index]}'", 'red'))
        else:
            print(colored(const.ERRORS[3], 'red'))


if __name__ == '__main__':
    main()
