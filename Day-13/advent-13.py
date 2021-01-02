"""
URL for challenge: https://adventofcode.com/2020/day/13
"""


from math import ceil, inf
from functools import reduce


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
    f = open("advent-13-input.txt")
    parsed_input = f.readlines()[1].strip().split(',')
    buses, offsets = [], []
    for idx, b_id in enumerate(parsed_input):
        if b_id != 'x':
            buses.append(int(b_id))
            offsets.append(idx)

    mod_values = [0]
    for bus_id, offset in zip(buses[1:], offsets[1:]):
        mod_values.append(bus_id - (offset % bus_id))

    w_values = []
    big_product = reduce(lambda x, y: x*y, buses)
    for bus_id in buses:
        z = int(big_product/bus_id)
        y = find_modulo_inverse(z % bus_id, bus_id)
        w_values.append(y * z)

    solution = 0
    for mod_val, w in zip(mod_values, w_values):
        solution += (mod_val * w)

    return solution % big_product


def find_modulo_inverse(target, modulus):
    """
    Find modulo inverse x of target wrt modulus
    such that target * x (mod modulus) == 1 using
    Euclid's extended algorithm.
    """
    a0, a1 = 0, 1
    b0, b1 = 1, 0
    while target != 0:
        quotient = modulus // target
        remainder = modulus % target
        modulus = target
        target = remainder

        a_tmp = a0 - quotient * a1
        a0 = a1
        a1 = a_tmp

        b_tmp = b0 - quotient * b1
        b0 = b1
        b1 = b_tmp

    return a0


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
