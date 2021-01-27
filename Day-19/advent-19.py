"""
URL for challenge: https://adventofcode.com/2020/day/19
"""


class Rule(object):
    def __init__(self, value, sub_rules):
        self.value = value
        self.sub_rules = sub_rules


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

        rules[rule_num] = Rule(rule_num, sub_rules)

    messages = [line.strip() for line in puzzle_input[index+1:]]

    return rules, messages


def part1():
    rules, messages = process_input()

    num_valid = 0
    for message in messages:
        if is_message_valid(message, '0', rules)[0]:
            num_valid += 1

    return num_valid


def is_message_valid(message, target_val, rules):
    if not message:
        return False, 0

    if target_val not in rules:
        return message[0] == target_val, 1

    rule = rules[target_val]
    msg_passes_any_rule = False
    for sub_rule in rule.sub_rules:
        idx = 0
        msg_passes_subrule = True
        for child_rule in sub_rule:
            sub_result = is_message_valid(message[idx:], child_rule, rules)
            msg_passes_subrule &= sub_result[0]
            idx += sub_result[1]
            if not msg_passes_subrule:
                break

        msg_passes_any_rule |= msg_passes_subrule
        if msg_passes_any_rule:
            break

    if target_val == '0' and message[idx:]:
        return False, 0

    return msg_passes_any_rule, idx


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
