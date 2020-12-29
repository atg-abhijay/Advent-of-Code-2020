"""
URL for challenge: https://adventofcode.com/2020/day/12
"""


def part1():
    f = open("advent-12-input.txt")
    commands = []
    for line in f.readlines():
        line = line.strip()
        commands.append((line[0], int(line[1:])))

    x_pos, y_pos = 0, 0
    current_dirn = 'E'
    for action, amount in commands:
        if action == 'F':
            x_pos, y_pos = move(x_pos, y_pos, amount, current_dirn)
        elif action in ['L', 'R']:
            current_dirn = rotate(current_dirn, action, amount)
        else:
            x_pos, y_pos = move(x_pos, y_pos, amount, action)

    return abs(x_pos) + abs(y_pos)


def rotate(current_dirn, rotate_dirn, amount):
    directions = ['N', 'E', 'S', 'W']
    clockwise_val = 1 if rotate_dirn == 'R' else -1
    movement = clockwise_val * int((amount/90))
    target_idx = (directions.index(current_dirn) + movement) % 4
    return directions[target_idx]


def move(x_pos, y_pos, amount, move_dirn):
    if move_dirn == 'N':
        y_pos += amount
    elif move_dirn == 'E':
        x_pos += amount
    elif move_dirn == 'S':
        y_pos -= amount
    elif move_dirn == 'W':
        x_pos -= amount

    return x_pos, y_pos


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
