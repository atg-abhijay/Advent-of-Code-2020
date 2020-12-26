"""
URL for challenge: https://adventofcode.com/2020/day/6
"""


class Adapter(object):
    def __init__(self, joltage):
        self.joltage = joltage
        self.children = []
        self.parents = []


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
    f = open("advent-10-input.txt")
    joltages = []
    for jolt in f.readlines():
        joltages.append(int(jolt.strip()))

    sorted_joltages = [0] + sorted(joltages)
    # Add device's built-in adapter
    sorted_joltages.append(sorted_joltages[-1] + 3)
    num_joltages = len(sorted_joltages)

    adapter_objs = {joltage: Adapter(joltage) for joltage in sorted_joltages}
    for idx, joltage in enumerate(sorted_joltages):
        adap = adapter_objs[joltage]
        idx += 1
        while True and idx < num_joltages:
            child_joltage = sorted_joltages[idx]
            if child_joltage - joltage <= 3:
                child_adap = adapter_objs[child_joltage]
                adap.children.append(child_joltage)
                child_adap.parents.append(joltage)
            else:
                break

            idx += 1

    return find_num_paths(adapter_objs[0], adapter_objs, {})


def find_num_paths(adap, adapter_objs, num_paths_dict):
    num_paths = 0
    num_paths_dict[adap.joltage] = num_paths
    if not adap.children:
        return 1

    for child_joltage in adap.children:
        child_adap = adapter_objs[child_joltage]
        if child_adap.joltage in num_paths_dict:
            num_paths += num_paths_dict[child_adap.joltage]
        else:
            num_paths += find_num_paths(child_adap, adapter_objs, num_paths_dict)

    num_paths_dict[adap.joltage] = num_paths
    return num_paths

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
