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
    """
    Replace candidate corrupt instructions
    (instructions with 'jmp' or 'nop')
    one-by-one and check if the program terminates.
    """
    instructions = process_input()
    corrupt_instr_idxs = run_instructions(instructions, False)[1]

    for corrupt_idx in corrupt_instr_idxs:
        instr = instructions[corrupt_idx][0]
        if instr == 'nop':
            instructions[corrupt_idx][0] = 'jmp'
        else:
            instructions[corrupt_idx][0] = 'nop'

        result = run_instructions(instructions, True)
        accumulator, does_prog_terminate = result[0], result[2]

        if does_prog_terminate:
            break
        else:
            # If program does not terminate,
            # put back the original instruction.
            instructions[corrupt_idx][0] = instr

    return accumulator


def run_instructions(instructions, check_prog_termination):
    """
    Return multiple entities so that Parts 1 and 2
    can use the entities that they need specifically.
    Iterate over the instructions and:
    - build up the accumulator
    - collect indices for instructions that may be corrupt
    - report if program terminates or not upon replacing
      a candidate corrupt instruction
    """
    num_instr = len(instructions)
    # Number of times an instruction is executed
    times_executed = [0 for x in range(num_instr)]
    # Indices for instructions that may be corrupt
    corrupt_instr_idxs = []
    accumulator, idx, does_prog_terminate = 0, 0, False

    while True:
        if check_prog_termination and idx >= num_instr:
            does_prog_terminate = True
            break

        instr, amount = instructions[idx]
        # If an instruction has already been executed,
        # the program will get stuck in a loop now.
        if times_executed[idx] > 0:
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

    return accumulator, corrupt_instr_idxs, does_prog_terminate


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
