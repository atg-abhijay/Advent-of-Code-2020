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


def create_tree(expression, nesting_depth):
    digits = set(string.digits)
    current_node = Node('+', nesting_depth)
    current_node.left_child = Node(0, nesting_depth)
    idx = 0

    while idx < len(expression):
        element = expression[idx]

        if set(element).issubset(digits):
            node = Node(int(element), nesting_depth)
            current_node.right_child = node

        elif element in ['+', '*']:
            node = Node(element, nesting_depth)
            node.left_child = current_node
            current_node = node

        elif element == '(':
            sub_result = create_tree(expression[idx+1:], nesting_depth+1)
            current_node.right_child = sub_result[0]
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


def part1():
    f = open("advent-18-input.txt")
    total_sum = 0
    for line in f.readlines():
        line = line.strip().split(' ')
        expression = []
        for elem in line:
            parsed_elem = re.split('([()])', elem)
            expression += [pe for pe in parsed_elem if pe]

        tree = create_tree(expression, 0)
        output = evaluate_tree(tree[0])
        total_sum += output

    return total_sum


def part2():
    return


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
