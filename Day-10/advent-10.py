"""
URL for challenge: https://adventofcode.com/2020/day/6
"""


def part1():
    """
    Since there is a way to use all adapters,
    none of them will be excluded. Sort them
    according to the joltages.

    Since all of them are used, all adapters
    will be within 3 joltages of each other and
    the sorting will help ensure that the next
    closest adapter is picked.
    """
    f = open("advent-10-input.txt")
    joltages = []
    for jolt in f.readlines():
        joltages.append(int(jolt.strip()))

    sorted_joltages = sorted(joltages)
    # Add device's built-in adapter
    sorted_joltages.append(sorted_joltages[-1] + 3)
    one_jolt_diffs, three_jolt_diffs = 0, 0
    # Charging outlet
    prev_jolt = 0

    for jolt in sorted_joltages:
        jolt_diff = jolt - prev_jolt
        if jolt_diff == 1:
            one_jolt_diffs += 1

        elif jolt_diff == 3:
            three_jolt_diffs += 1

        prev_jolt = jolt

    return one_jolt_diffs * three_jolt_diffs


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
