"""
URL for challenge: https://adventofcode.com/2020/day/19

Check PR description for brief notes and comments.
"""


class Rule(object):
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

        rules[rule_num] = Rule(rule_num, sub_rules)

    messages = [line.strip() for line in puzzle_input[index+1:]]

    return rules, messages


def part1():
    rules, messages = process_input()

    num_valid = 0
    for message in messages:
        is_valid, latest_idx = is_message_valid(message, '0', rules)
        # If a portion of the message is left over
        # after iterating through the rules, then
        # those are extra characters and the
        # message is not valid.
        if is_valid and not message[latest_idx:]:
            num_valid += 1

    return num_valid


def build_strings(rule_val, rules):
    """
    Return a list of strings that
    are valid for the given rule.
    """
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
    """
    Rule 0 produces strings that are of the form -
              (42)x (42)y (31)y
    where rules 42 and 31 produce a constant list
    of strings having the same lengths. x and y
    denote the number of repetitions of those rules.
    Any string that follows rule 0 must have the above form.
    """
    rules, messages = process_input()

    num_valid = 0
    strings_42 = set(build_strings('42', rules))
    strings_31 = set(build_strings('31', rules))
    elem = strings_42.pop()
    str_len = len(elem)
    strings_42.add(elem)

    for message in messages:
        appearances_42, appearances_31 = 0, 0
        is_valid = True
        while message:
            sub_message = message[:str_len]
            if sub_message in strings_42:
                appearances_42 += 1
            elif sub_message in strings_31:
                break
            else:
                is_valid = False
                break

            message = message[str_len:]

        while message:
            sub_message = message[:str_len]
            if sub_message in strings_31:
                appearances_31 += 1

            else:
                is_valid = False
                break

            message = message[str_len:]

        if not is_valid:
            continue
        elif appearances_31 >= appearances_42:
            continue
        elif appearances_31 == 0:
            continue

        num_valid += 1

    return num_valid


def is_message_valid(message, target_val, rules):
    # If there are rules to follow but
    # the message is empty, the message
    # is shorter than required.
    if not message:
        return False, 0

    # The alphabets will not
    # be in the dictionary.
    if target_val not in rules:
        return message[0] == target_val, 1

    # The message has to completely pass
    # a sub-rule. The message has to pass
    # at least one of the sub-rules.
    rule = rules[target_val]
    msg_passes_any_rule = False
    for sub_rule in rule.sub_rules:
        latest_idx = 0
        msg_passes_subrule = True
        for child_rule in sub_rule:
            sub_result = is_message_valid(
                message[latest_idx:], child_rule, rules)
            msg_passes_subrule &= sub_result[0]
            latest_idx += sub_result[1]
            if not msg_passes_subrule:
                break

        msg_passes_any_rule |= msg_passes_subrule
        if msg_passes_any_rule:
            break

    return msg_passes_any_rule, latest_idx


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
