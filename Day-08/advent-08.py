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
    accumulator = run_instructions(instructions, False)[0]
    return accumulator


def part2():
    instructions = process_input()
    corrupt_instr_idxs = run_instructions(instructions, False)[1]

    for corrupt_idx in corrupt_instr_idxs:
        corrupt_instr = instructions[corrupt_idx][0]
        if corrupt_instr == 'nop':
            instructions[corrupt_idx][0] = 'jmp'
        else:
            instructions[corrupt_idx][0] = 'nop'

        result = run_instructions(instructions, True)
        accumulator, should_stop = result[0], result[2]

        if should_stop:
            instructions[corrupt_idx][0] = corrupt_instr
        else:
            break

    return accumulator


def run_instructions(instructions, check_termination):
    num_instr = len(instructions)
    times_executed = [0 for x in range(num_instr)]
    accumulator, idx, should_stop = 0, 0, False
    corrupt_instr_idxs = []

    while not should_stop:
        if check_termination and idx >= num_instr:
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
            corrupt_instr_idxs.append(idx)
            idx += amount

        else:
            corrupt_instr_idxs.append(idx)
            idx += 1

    return accumulator, corrupt_instr_idxs, should_stop


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
