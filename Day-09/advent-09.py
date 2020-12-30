"""
URL for challenge: https://adventofcode.com/2020/day/9
"""


def process_input():
    f = open("advent-09-input.txt")
    input_nums = []
    for line in f.readlines():
        input_nums.append(int(line.strip()))

    return input_nums


def part1():
    input_nums = process_input()
    preamble_size = 25
    preamble = set(input_nums[:preamble_size])

    idx_to_remove = -1
    target_num = 0
    for num in input_nums[preamble_size:]:
        # Update the preamble to keep
        # track of last 25 numbers
        if idx_to_remove != -1:
            preamble.remove(input_nums[idx_to_remove])

        # If the number can be formed using the
        # last 25 numbers, the intersection will be
        # of size at least 2.
        complement_set = set(num - val for val in preamble)
        intxn_size = len(preamble.intersection(complement_set))
        if intxn_size < 2:
            target_num = num
            break

        preamble.add(num)
        idx_to_remove += 1

    return target_num


def part2():
    input_nums = process_input()
    invalid_num = part1()
    invalid_idx = input_nums.index(invalid_num)
    sub_list = input_nums[:invalid_idx]
    sub_list_size = len(sub_list)

    current_idx, current_sum = 0, 0
    start_idx, end_idx = 0, 0
    target_list = []
    while True and current_idx < sub_list_size:
        if current_sum == invalid_num:
            target_list = sub_list[start_idx:end_idx+1]
            break

        new_sum = current_sum + sub_list[current_idx]
        while new_sum > invalid_num:
            new_sum -= sub_list[start_idx]
            start_idx += 1

        current_sum = new_sum
        end_idx = current_idx
        current_idx += 1

    sorted_targets = sorted(target_list)
    return sorted_targets[0] + sorted_targets[-1]


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
