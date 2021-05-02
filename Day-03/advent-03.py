"""
URL for challenge: https://adventofcode.com/2020/day/3
"""


from functools import reduce
from operator import mul


def process_input():
    f = open("advent-03-input.txt")
    return [list(row.strip()) for row in f.readlines()]


def part1(grid, right_mvmt, down_mvmt):
    num_rows, num_cols = len(grid), len(grid[0])
    current_row, current_col, num_trees = 0, 0, 0

    while current_row < num_rows:
        if grid[current_row][current_col] == '#':
            num_trees += 1

        current_col = (current_col + right_mvmt) % num_cols
        current_row += down_mvmt

    return num_trees


def part2():
    grid = process_input()
    trees_encounterd = map(lambda slope: part1(grid, *slope),
                           [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])
    return reduce(mul, trees_encounterd)


def run():
    chall = int(input("Please enter either 1 or 2 for the challenges: "))
    if chall == 1:
        print(part1(process_input(), 3, 1))
    elif chall == 2:
        print(part2())
    else:
        print("You need to enter either 1 or 2")
        exit(1)


run()
