"""
URL for challenge: https://adventofcode.com/2020/day/3
"""


def process_input():
    f = open("advent-03-input.txt")
    grid = []
    for row in f.readlines():
        grid.append(list(row.strip()))

    num_rows = len(grid)
    num_cols = len(grid[0])

    return [grid, num_rows, num_cols]


def part1(input_details, right_mvmt, down_mvmt):
    grid, num_rows, num_cols = input_details
    current_row, current_col, num_trees = 0, 0, 0

    while current_row < num_rows:
        if grid[current_row][current_col] == '#':
            num_trees += 1

        current_col = (current_col + right_mvmt) % num_cols
        current_row += down_mvmt

    return num_trees


def part2():
    result = 1
    input_details = process_input()
    result *= part1(input_details, 1, 1)
    result *= part1(input_details, 3, 1)
    result *= part1(input_details, 5, 1)
    result *= part1(input_details, 7, 1)
    result *= part1(input_details, 1, 2)

    return result


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
