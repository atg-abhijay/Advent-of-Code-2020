"""
URL for challenge: https://adventofcode.com/2020/day/1
"""

from functools import reduce

def process_input():
    f = open("advent-01-input.txt")
    amounts = []
    for line in f.readlines():
        amounts.append(int(line))

    return amounts

def part1(target_amount, amounts):
    """
    Calculate the inverse of the given amounts
    (2020 - amount). By creating sets for them
    and taking the intersection, the only amounts
    that will be left are x and (2020 - x).
    """
    inverse_amounts = [target_amount - x for x in amounts]
    pair_entries = (set(amounts)).intersection(set(inverse_amounts))
    num_entries = len(pair_entries)

    if num_entries == 1:
        return pair_entries.pop() ** 2

    elif num_entries == 2:
        return reduce(lambda x, y: x*y, pair_entries)

    return None

def part2():
    amounts = process_input()
    inverse_amounts = [2020 - x for x in amounts]

    for idx, inv in enumerate(inverse_amounts):
        sub_solution = part1(inv, amounts[:idx] + amounts[idx+1:])
        if sub_solution is not None:
            return amounts[idx] * sub_solution

def run():
    chall = int(input("Please enter either 1 or 2 for the challenges: "))
    if chall == 1:
        print(part1(2020, process_input()))
    elif chall == 2:
        print(part2())
    else:
        print("You need to enter either 1 or 2")
        exit(1)

run()
