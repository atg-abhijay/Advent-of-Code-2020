"""
URL for challenge: https://adventofcode.com/2020/day/23
"""


from networkx import add_cycle, add_path, DiGraph
from tqdm import tqdm


def process_input():
    f = open("advent-23-input.txt")
    return [int(x) for x in f.readline()]


def part1():
    cups = process_input()
    circle = play_game(cups, 100, cups[0], min(cups), max(cups))

    cup, result_cups = next(circle.successors(1)), []
    while cup != 1:
        result_cups.append(str(cup))
        cup = next(circle.successors(cup))

    return ''.join(result_cups)


def part2():
    return


def play_game(cups, num_moves, current_cup, lowest_cup, highest_cup):
    circle = DiGraph()
    add_cycle(circle, cups)

    for _ in tqdm(range(num_moves)):
        neighbours = pick_up_cups(circle, current_cup)
        destn_cup = find_destination_cup(circle, current_cup, lowest_cup, highest_cup)
        place_cups(circle, destn_cup, neighbours)
        current_cup = next(circle.successors(current_cup))

    return circle


def pick_up_cups(circle, current_cup):
    starting_cup, num_pickups = current_cup, 3
    neighbours = []
    for _ in range(num_pickups):
        neighbour = next(circle.successors(starting_cup))
        neighbours.append(neighbour)
        starting_cup = neighbour

    circle.add_edge(current_cup, next(circle.successors(starting_cup)))
    circle.remove_nodes_from(neighbours)

    return neighbours


def find_destination_cup(circle, current_cup, lowest_cup, highest_cup):
    destination_cup = current_cup - 1
    while 1:
        if destination_cup in circle:
            return destination_cup

        destination_cup -= 1
        if destination_cup < lowest_cup:
            destination_cup = highest_cup


def place_cups(circle, destination_cup, neighbours):
    current_nb = next(circle.successors(destination_cup))
    add_path(circle, neighbours)
    circle.remove_edge(destination_cup, current_nb)
    circle.add_edge(destination_cup, neighbours[0])
    circle.add_edge(neighbours[-1], current_nb)


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
