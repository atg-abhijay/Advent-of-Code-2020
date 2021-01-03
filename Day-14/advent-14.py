"""
URL for challenge: https://adventofcode.com/2020/day/14
"""


def process_input():
    f = open("advent-14-input.txt")
    instructions = []
    for line in f.readlines():
        fields = line.strip().split(' = ')
        if fields[0] == "mask":
            instructions.append(("mask", fields[1]))
        else:
            address = int(fields[0][4:-1])
            instructions.append(("mem", address, int(fields[1])))

    return instructions


def part1():
    instructions = process_input()
    mask_with_zeroes, mask_with_ones = 0, 0
    addresses = {}
    for instr in instructions:
        command = instr[0]
        if command == "mask":
            mask_with_zeroes = int(instr[1].replace('X', '0'), 2)
            mask_with_ones = int(instr[1].replace('X', '1'), 2)
        else:
            value = instr[2]
            addresses[instr[1]] = (value | mask_with_zeroes) & mask_with_ones

    return sum(addresses.values())


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
