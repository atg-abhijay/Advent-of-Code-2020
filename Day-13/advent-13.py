"""
URL for challenge: https://adventofcode.com/2020/day/13
"""


from math import ceil, inf


def part1():
    f = open("advent-13-input.txt")
    input_lines = f.readlines()
    departure_estimate = int(input_lines[0].strip())
    parsed_input = input_lines[1].strip().split(',')
    bus_ids = [int(b_id) for b_id in parsed_input if b_id != 'x']

    earliest_bus, smallest_diff = 0, inf
    for b_id in bus_ids:
        multiplicator = ceil(departure_estimate/b_id)
        diff = b_id * multiplicator - departure_estimate
        if diff < smallest_diff:
            smallest_diff = diff
            earliest_bus = b_id

    return earliest_bus * smallest_diff


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
