"""
URL for challenge: https://adventofcode.com/2020/day/8
"""


def process_input():
    f = open("/Users/AbhijayGupta/Projects/Advent-of-Code-2020/Day-08/advent-08-input.txt")
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
    instructions = process_input()
    times_executed = [0 for x in range(len(instructions))]
    idx, should_stop = 0, False
    corrupt_instr_idxs = []
    corrupted_instr = []
    while not should_stop:
        instr, amount = instructions[idx]
        if times_executed[idx] > 0:
            break

        times_executed[idx] += 1
        if instr == 'acc':
            idx += 1

        elif instr == 'jmp':
            corrupt_instr_idxs.append(idx)
            idx += amount

        else:
            corrupt_instr_idxs.append(idx)
            idx += 1

    for corrupt_idx in corrupt_instr_idxs:
        corrupt_instr = instructions[corrupt_idx][0]
        if corrupt_instr == 'nop':
            instructions[corrupt_idx][0] = 'jmp'
        else:
            instructions[corrupt_idx][0] = 'nop'

        times_executed = [0 for x in range(len(instructions))]
        accumulator, idx, should_stop = 0, 0, False
        while not should_stop:
            if idx >= len(instructions):
                break

            instr, amount = instructions[idx]
            if times_executed[idx] > 0:
                should_stop = True
                break

            times_executed[idx] += 1
            if instr == 'acc':
                accumulator += amount
                idx += 1

            elif instr == 'jmp':
                idx += amount

            else:
                idx += 1

        if should_stop:
            instructions[corrupt_idx][0] = corrupt_instr
        else:
            break

    return accumulator


    # if corrupted_instr[0] == 'jmp':
    #     instructions[pred_idx][0] = 'nop'
    # else:
    #     instructions[pred_idx][0] = 'jmp'

    # accumulator, idx, should_stop = 0, 0, False
    # num_instr = len(instructions)
    # while not should_stop:
    #     if idx >= num_instr:
    #         break

    #     instr, amount = instructions[idx]
    #     if instr == 'acc':
    #         accumulator += amount
    #         idx += 1

    #     elif instr == 'jmp':
    #         idx += amount

    #     else:
    #         idx += 1

    # return accumulator


def run():
    chall = int(input("Please enter either 1 or 2 for the challenges: "))
    # chall = 2
    if chall == 1:
        print(part1())
    elif chall == 2:
        print(part2())
    else:
        print("You need to enter either 1 or 2")
        exit(1)


run()
