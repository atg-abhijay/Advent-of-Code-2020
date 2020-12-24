"""
URL for challenge: https://adventofcode.com/2020/day/8
"""


def process_input():
    f = open("advent-08-input.txt")
    instructions = []
    for line in f.readlines():
        line = line.strip().split(sep=' ')
        instr, amount = line[0], int(line[1])
        instructions.append([instr, amount])

    return instructions


def part1():
    instructions = process_input()
    times_executed = [0 for x in range(len(instructions))]
    accumulator, idx, should_stop = 0, 0, False
    while not should_stop:
        instr, amount = instructions[idx]
        if times_executed[idx] > 0:
            break

        times_executed[idx] += 1
        if instr == 'acc':
            accumulator += amount
            idx += 1

        elif instr == 'jmp':
            idx += amount

        else:
            idx += 1

    return accumulator


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
