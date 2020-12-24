"""
URL for challenge: https://adventofcode.com/2020/day/6
"""

import string


def part1():
    f = open("advent-06-input.txt")
    group_counts = []
    yes_answers = set()
    for person_answers in f.readlines():
        if person_answers == '\n':
            group_counts.append(len(yes_answers))
            yes_answers.clear()
            continue

        person_answers = person_answers.strip()
        yes_answers = yes_answers.union(set(person_answers))

    group_counts.append(len(yes_answers))
    return sum(group_counts)


def part2():
    f = open("advent-06-input.txt")
    group_counts = []
    yes_answers = set(string.ascii_lowercase)
    for person_answers in f.readlines():
        if person_answers == '\n':
            group_counts.append(len(yes_answers))
            yes_answers = set(string.ascii_lowercase)
            continue

        person_answers = person_answers.strip()
        yes_answers = yes_answers.intersection(set(person_answers))

    group_counts.append(len(yes_answers))
    return sum(group_counts)


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
