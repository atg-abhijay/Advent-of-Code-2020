"""
URL for challenge: https://adventofcode.com/2020/day/19
"""


class Node(object):
    def __init__(self, value, sub_rules):
        self.value = value
        self.sub_rules = sub_rules
        self.strings = []


def process_input():
    f = open("advent-19-input.txt")
    index, rules = 0, {}
    puzzle_input = f.readlines()
    for index, line in enumerate(puzzle_input):
        if line == '\n':
            break

        line = line.strip().split(': ')
        rule_num = line[0]
        sub_rules = []
        sub_rule_sequences = line[1].split(' | ')
        for sub_rule in sub_rule_sequences:
            sub_rules.append([x.replace('"', '') for x in sub_rule.split()])

        rules[rule_num] = Node(rule_num, sub_rules)

    messages = [line.strip() for line in puzzle_input[index+1:]]

    return rules, messages


def part1():
    rules, messages = process_input()
    all_strings = set(build_strings('0', rules))

    num_valid = 0
    for message in messages:
        if message in all_strings:
            num_valid += 1

    return num_valid


def build_strings(rule_val, rules):
    if rule_val not in rules:
        return [rule_val]

    rule = rules[rule_val]
    if rule.strings:
        return rule.strings

    for sub_rule in rule.sub_rules:
        sub_rule_strings = []
        for next_rule in sub_rule:
            child_strings = build_strings(next_rule, rules)
            if not sub_rule_strings:
                sub_rule_strings = child_strings.copy()
            else:
                current_strings = sub_rule_strings.copy()
                sub_rule_strings.clear()
                for s in current_strings:
                    for t in child_strings:
                        sub_rule_strings.append(s + t)

        rule.strings += sub_rule_strings

    return rule.strings


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
