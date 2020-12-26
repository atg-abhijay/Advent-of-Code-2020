"""
URL for challenge: https://adventofcode.com/2020/day/11
"""


def process_input():
    """
    Since the rules are applied to all seats
    simultaneously, two grids will be required
    since the original grid cannot be edited
    whilst the rules are being applied.
    """
    f = open("advent-11-input.txt")
    # Create a boundary of 'floor' tiles that
    # surrounds the original input to avoid having
    # to check for index out of bounds for corner cases.
    grid_before_rules = []
    for row in f.readlines():
        seats = ['.'] + list(row.strip()) + ['.']
        grid_before_rules.append(seats)

    grid_before_rules = [['.' for x in range(
        len(seats))]] + grid_before_rules + [['.' for x in range(len(seats))]]

    num_rows, num_cols = len(grid_before_rules), len(grid_before_rules[0])
    grid_after_rules = [['.' for x in range(num_cols)] for y in range(num_rows)]

    return grid_before_rules, grid_after_rules, num_rows, num_cols


def part1():
    grid_before_rules, grid_after_rules, num_rows, num_cols = process_input()

    # Only stop once the application of
    # the rules produces no changes in state
    while True:
        # Since a boundary was added to the original grid,
        # the indices are as such to process only the original grid
        for row_idx in range(1, num_rows - 1):
            for col_idx in range(1, num_cols - 1):
                seat_state = grid_before_rules[row_idx][col_idx]
                num_neighbours = check_neighbours(row_idx, col_idx, grid_before_rules)

                if seat_state == 'L' and num_neighbours == 0:
                    grid_after_rules[row_idx][col_idx] = '#'

                elif seat_state == '#' and num_neighbours >= 4:
                    grid_after_rules[row_idx][col_idx] = 'L'

        # 1. Check if applying the rules changed the grid
        # 2. Copy the 'after' grid to the 'before' grid in
        #    preparation for the next iteration of rules
        is_grid_unchanged = True
        for row_idx in range(1, num_rows - 1):
            for col_idx in range(1, num_cols - 1):
                val_after = grid_after_rules[row_idx][col_idx]
                is_val_unchanged = grid_before_rules[row_idx][col_idx] == val_after
                is_grid_unchanged = is_grid_unchanged and is_val_unchanged
                grid_before_rules[row_idx][col_idx] = val_after

        if is_grid_unchanged:
            break

    num_occupied_seats = 0
    for row_idx in range(1, num_rows - 1):
        for col_idx in range(1, num_cols - 1):
            if grid_after_rules[row_idx][col_idx] == '#':
                num_occupied_seats += 1

    return num_occupied_seats


def check_neighbours(row_idx, col_idx, grid):
    neighbour_indices = {"North": (row_idx-1, col_idx), "North-East": (row_idx-1, col_idx+1),
                         "East": (row_idx, col_idx+1), "South-East": (row_idx+1, col_idx+1),
                         "South": (row_idx+1, col_idx), "South-West": (row_idx+1, col_idx-1),
                         "West": (row_idx, col_idx-1), "North-West": (row_idx-1, col_idx-1)}
    num_neighbours = 0
    for nb_row, nb_col in neighbour_indices.values():
        if grid[nb_row][nb_col] == '#':
            num_neighbours += 1

    return num_neighbours


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
