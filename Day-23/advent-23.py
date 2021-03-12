"""
URL for challenge: https://adventofcode.com/2020/day/23

Check PR description for some brief notes.
"""


from tqdm import tqdm


def process_input():
    f = open("advent-23-input.txt")
    input_cups = [int(x) for x in f.readline()]
    highest_cup = len(input_cups)
    # 1. Let element at index 0 be a dummy value so that cup labels and
    #    indices match up. At the beginning, all neighbours are set to -1.
    # 2. neighbours[cup] = clockwise cup neighbour
    neighbours = [-1 for x in range(highest_cup+1)]
    for idx, cup in enumerate(input_cups[:-1]):
        neighbours[cup] = input_cups[idx+1]

    neighbours[input_cups[-1]] = input_cups[0]

    return neighbours, input_cups, highest_cup


def part1():
    neighbours, input_cups, highest_cup = process_input()
    play_game(neighbours, 100, input_cups[0], highest_cup)

    cup, result_cups = neighbours[1], []
    while cup != 1:
        result_cups.append(str(cup))
        cup = neighbours[cup]

    return ''.join(result_cups)


def part2():
    # Note: Takes about 25 seconds to run
    # 1. Last cup from puzzle input will connect to first cup from increasing list.
    # 2. From increasing list, cup x will connect to cup (x+1).
    # 3. Last cup from increasing list (1 millionth cup) will connect to very first cup.
    neighbours, input_cups, current_max = process_input()
    neighbours[input_cups[-1]] = current_max+1
    neighbours.extend([x+1 for x in range(current_max+1, 1_000_001)])
    neighbours[-1] = input_cups[0]

    play_game(neighbours, 10_000_000, input_cups[0], 1_000_000)
    first_num = neighbours[1]

    return first_num * neighbours[first_num]


def play_game(neighbours, num_moves, current_cup, highest_cup):
    for _ in tqdm(range(num_moves)):
        target_cups = pick_up_cups(neighbours, current_cup)
        destn_cup = find_destination_cup(neighbours, current_cup, highest_cup)
        place_cups(neighbours, destn_cup, target_cups)
        current_cup = neighbours[current_cup]


def pick_up_cups(neighbours, current_cup):
    starting_cup, num_pickups = current_cup, 3
    target_cups = []
    for _ in range(num_pickups):
        target_cup = neighbours[starting_cup]
        target_cups.append(target_cup)
        starting_cup = target_cup

    neighbours[current_cup] = neighbours[target_cup]
    # Set their neighbours to -1 so that they are completely disconnected
    # from everything. Their internal order will still be maintained with
    # the list target_cups.
    for target_cup in target_cups:
        neighbours[target_cup] = -1

    return target_cups


def find_destination_cup(neighbours, current_cup, highest_cup):
    lowest_cup = 1
    destination_cup = current_cup - 1
    while 1:
        # Disconnected cups have '-1' neighbours
        if neighbours[destination_cup] != -1:
            return destination_cup

        destination_cup -= 1
        if destination_cup < lowest_cup:
            destination_cup = highest_cup


def place_cups(neighbours, destination_cup, target_cups):
    current_nb = neighbours[destination_cup]
    for target_cup in target_cups:
        neighbours[destination_cup] = target_cup
        destination_cup = target_cup

    neighbours[destination_cup] = current_nb


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
