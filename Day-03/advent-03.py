"""
URL for challenge: https://adventofcode.com/2020/day/3
"""

def part1():
    f = open("advent-03-input.txt")
    grid = []
    for row in f.readlines():
        grid.append(list(row.strip()))

    num_rows = len(grid)
    num_cols = len(grid[0])
    current_row, current_col, num_trees = 0, 0, 0

    while current_row < num_rows:
        if grid[current_row][current_col] == '#':
            num_trees += 1

        current_col = (current_col + 3) % num_cols
        current_row += 1

    return num_trees

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
