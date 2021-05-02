"""
URL for challenge: https://adventofcode.com/2020/day/15
"""


from tqdm import trange


def part1(stop_turn):
    f = open("advent-15-input.txt")
    starting_nums = list(map(int, f.readline().strip().split(',')))
    unique_nums = {num: idx+1 for idx, num in enumerate(starting_nums)}
    # Add a dummy value so that the
    # indices and turns match up
    turn_vals = [-1] + starting_nums

    start_turn = len(starting_nums) + 1
    for current_turn in trange(start_turn, stop_turn+1):
        prev_num = turn_vals[-1]
        if prev_num not in unique_nums:
            unique_nums[prev_num] = current_turn - 1
            turn_vals.append(0)
        else:
            last_known_turn = unique_nums[prev_num]
            turns_apart = (current_turn - 1) - last_known_turn
            unique_nums[prev_num] = current_turn - 1
            turn_vals.append(turns_apart)

    return turn_vals[-1]


def part2(stop_turn):
    # Takes about 30 seconds to run
    return part1(stop_turn)


def run():
    chall = int(input("Please enter either 1 or 2 for the challenges: "))
    if chall == 1:
        print(part1(2020))
    elif chall == 2:
        print(part2(30_000_000))
    else:
        print("You need to enter either 1 or 2")
        exit(1)


run()
