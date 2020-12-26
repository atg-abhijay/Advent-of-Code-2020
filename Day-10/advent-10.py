"""
URL for challenge: https://adventofcode.com/2020/day/10
"""

from typing import List


class Adapter(object):
    def __init__(self, joltage):
        self.joltage: int = joltage
        self.children: List[Adapter] = []
        # number of paths from this
        # adapter to the device
        self.num_paths = 0


def process_input():
    f = open("advent-10-input.txt")
    # Add charging outlet
    joltages = [0]
    for jolt in f.readlines():
        joltages.append(int(jolt.strip()))

    sorted_joltages = sorted(joltages)
    # Add device's built-in adapter
    sorted_joltages.append(sorted_joltages[-1] + 3)
    return sorted_joltages


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
    sorted_joltages = process_input()
    one_jolt_diffs, three_jolt_diffs = 0, 0
    # Charging outlet
    prev_jolt = sorted_joltages[0]

    for jolt in sorted_joltages[1:]:
        jolt_diff = jolt - prev_jolt
        if jolt_diff == 1:
            one_jolt_diffs += 1

        elif jolt_diff == 3:
            three_jolt_diffs += 1

        prev_jolt = jolt

    return one_jolt_diffs * three_jolt_diffs


def part2():
    sorted_joltages = process_input()
    num_joltages = len(sorted_joltages)
    adapters_dict = {joltage: Adapter(joltage) for joltage in sorted_joltages}

    for idx, joltage in enumerate(sorted_joltages):
        adapter = adapters_dict[joltage]
        idx += 1
        while True and idx < num_joltages:
            child_joltage = sorted_joltages[idx]
            if child_joltage - joltage <= 3:
                adapter.children.append(adapters_dict[child_joltage])
            else:
                break

            idx += 1

    return find_num_paths(adapters_dict[0])


def find_num_paths(adapter):
    """
    Perform a DFS and find the number of
    paths possible from an adapter.
    """
    if not adapter.children:
        adapter.num_paths = 1
        return adapter.num_paths

    for child_adapter in adapter.children:
        if child_adapter.num_paths:
            adapter.num_paths += child_adapter.num_paths
        else:
            adapter.num_paths += find_num_paths(child_adapter)

    return adapter.num_paths


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
