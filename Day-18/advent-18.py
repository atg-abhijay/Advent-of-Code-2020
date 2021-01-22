"""
URL for challenge: https://adventofcode.com/2020/day/18
"""


import string, re


class Node(object):
    def __init__(self, value, depth):
        self.value = value
        self.nesting_depth = depth
        self.left_child = None
        self.right_child = None
        self.parent = None


def process_input():
    f = open("advent-18-input.txt")
    expressions = []
    for line in f.readlines():
        line = line.strip().split(' ')
        expression = []
        for elem in line:
            parsed_elem = re.split('([()])', elem)
            expression += [pe for pe in parsed_elem if pe]

        expressions.append(expression)

    return expressions


def part1():
    expressions = process_input()
    total_sum = 0
    for expression in expressions:
        tree = create_tree(expression, 0)[0]
        total_sum += evaluate_tree(tree)

    return total_sum


def part2():
    expressions = process_input()
    total_sum = 0
    for expression in expressions:
        tree = create_tree(expression, 0)[0]
        rearrange_nodes(tree)
        root_node = get_root_node(tree)
        total_sum += evaluate_tree(root_node)

    return total_sum


def create_tree(expression, nesting_depth):
    digits = set(string.digits)
    current_node = Node('+', nesting_depth)
    current_node.left_child = Node(0, nesting_depth)
    current_node.left_child.parent = current_node
    idx = 0

    while idx < len(expression):
        element = expression[idx]

        if set(element).issubset(digits):
            node = Node(int(element), nesting_depth)
            current_node.right_child = node
            node.parent = current_node

        elif element in ['+', '*']:
            node = Node(element, nesting_depth)
            node.left_child = current_node
            current_node.parent = node
            current_node = node

        elif element == '(':
            sub_result = create_tree(expression[idx+1:], nesting_depth+1)
            current_node.right_child = sub_result[0]
            sub_result[0].parent = current_node
            idx += sub_result[1]

        else:
            return current_node, idx + 1

        idx += 1

    return current_node, idx


def evaluate_tree(node):
    if not node:
        return 0

    if not node.left_child and not node.right_child:
        return node.value

    if node.value == '+':
        return evaluate_tree(node.left_child) + evaluate_tree(node.right_child)
    elif node.value == '*':
        return evaluate_tree(node.left_child) * evaluate_tree(node.right_child)


def get_root_node(node):
    if not node.parent:
        return node

    return get_root_node(node.parent)


def rearrange_nodes(node):
    if not node.left_child and not node.right_child:
        return node

    rearrange_nodes(node.right_child)
    rearrange_nodes(node.left_child)

    left_child = node.left_child
    if node.value == '+' and left_child.value == '*':
        if node.parent:
            if node == node.parent.left_child:
                node.parent.left_child = left_child
            else:
                node.parent.right_child = left_child

        left_child.parent = node.parent

        node.left_child = left_child.right_child
        left_child.right_child.parent = node

        left_child.right_child = node
        node.parent = left_child

    return node


def run():
    chall = int(input("Please enter either 1 or 2 for the challenges: "))
    if chall == 1:
        print(part1())
    elif chall == 2:
        print(part2())
    else:
        print("You need to enter either 1 or 2")
        exit(1)


run()
