"""
URL for challenge: https://adventofcode.com/2020/day/24
"""


def process_input():
    f = open("advent-24-input.txt")
    all_directions = []
    for line in f.readlines():
        line, directions = line.strip(), []
        step, is_north_south = '', False
        for char in line:
            if char in ['n', 's']:
                step, is_north_south = char, True
            else:
                if is_north_south:
                    directions.append(step + char)
                    step, is_north_south = '', False
                else:
                    directions.append(char)

        all_directions.append(directions)

    return all_directions


def part1():
    return


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
