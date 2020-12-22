"""
URL for challenge: https://adventofcode.com/2020/day/1
"""

from functools import reduce

def part1():
    f = open("advent-01-input.txt")
    amounts = set()
    inverse_amounts = set()
    for line in f.readlines():
        amount = int(line)
        amounts.add(amount)
        inverse_amounts.add(2020-amount)

    pair_entries = amounts.intersection(inverse_amounts)
    print(reduce(lambda x, y: x*y, pair_entries))

def part2():
    return

def run():
    chall = int(input("Please enter either 1 or 2 for the challenges: "))
    if chall == 1:
        part1()
    elif chall == 2:
        part2()
    else:
        print("You need to enter either 1 or 2")
        exit(1)

run()
