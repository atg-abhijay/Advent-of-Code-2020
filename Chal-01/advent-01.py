"""
URL for challenge: https://adventofcode.com/2020/day/1
"""

from functools import reduce

def part1():
    """
    Calculate the inverse of the given amounts
    (2020 - amount). By creating sets for them
    and taking the intersection, the only amounts
    that will be left are x and (2020 - x).
    """
    f = open("advent-01-input.txt")
    amounts = set()
    inverse_amounts = set()
    for line in f.readlines():
        amount = int(line)
        amounts.add(amount)
        inverse_amounts.add(2020-amount)

    pair_entries = amounts.intersection(inverse_amounts)
    if len(pair_entries) == 1:
        return pair_entries.pop() ** 2

    return reduce(lambda x, y: x*y, pair_entries)

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
