"""
URL for challenge: https://adventofcode.com/2020/day/12
"""


from math import sin, cos, radians


def process_input():
    f = open("advent-12-input.txt")
    commands = []
    for line in f.readlines():
        line = line.strip()
        commands.append((line[0], int(line[1:])))

    return commands


def part1():
    commands = process_input()
    x_pos, y_pos = 0, 0
    current_dirn = 'E'
    for action, amount in commands:
        if action == 'F':
            x_pos, y_pos = move(x_pos, y_pos, amount, current_dirn)
        elif action in ['L', 'R']:
            current_dirn = turn(current_dirn, action, amount)
        else:
            x_pos, y_pos = move(x_pos, y_pos, amount, action)

    return abs(x_pos) + abs(y_pos)


def turn(current_dirn, turn_dirn, amount):
    directions = ['N', 'E', 'S', 'W']
    clockwise_val = 1 if turn_dirn == 'R' else -1
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
    commands = process_input()
    ship_x, ship_y = 0, 0
    waypoint_x, waypoint_y = 10, 1
    for action, amount in commands:
        if action == 'F':
            ship_x += (waypoint_x * amount)
            ship_y += (waypoint_y * amount)
        elif action in ['L', 'R']:
            waypoint_x, waypoint_y = turn_waypoint(waypoint_x, waypoint_y, action, amount)
        else:
            waypoint_x, waypoint_y = move(waypoint_x, waypoint_y, amount, action)

    return abs(ship_x) + abs(ship_y)


def turn_waypoint(waypoint_x, waypoint_y, turn_dirn, amount):
    # Note: Check PR description for this method
    is_clockwise = 1 if turn_dirn == 'R' else -1
    amount = radians(amount * is_clockwise)
    # Use a rotation matrix where
    # [x'] = [ cos A  sin A] [x]
    # [y']   [-sin A  cos A] [y]
    cos_val = int(cos(amount))
    sin_val = int(sin(amount))
    new_waypoint_x = waypoint_x * cos_val + waypoint_y * sin_val
    new_waypoint_y = -1 * waypoint_x * sin_val + waypoint_y * cos_val
    return new_waypoint_x, new_waypoint_y


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
