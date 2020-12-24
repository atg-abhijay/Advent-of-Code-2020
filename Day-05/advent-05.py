"""
URL for challenge: https://adventofcode.com/2020/day/5
"""


def generate_rows_cols():
    f = open("advent-05-input.txt")
    seat_rows, seat_cols = [], []
    for line in f.readlines():
        seat = line.strip()
        row_code = seat[:7]
        binary_row = ["1" if x == "B" else "0" for x in row_code]
        seat_rows.append(int(''.join(binary_row), 2))

        col_code = seat[7:]
        binary_col = ["1" if x == "R" else "0" for x in col_code]
        seat_cols.append(int(''.join(binary_col), 2))

    return seat_rows, seat_cols


def part1():
    seat_rows, seat_cols = generate_rows_cols()
    highest_seat_id = 0
    for row, col in zip(seat_rows, seat_cols):
        seat_id = row * 8 + col
        if seat_id > highest_seat_id:
            highest_seat_id = seat_id

    return highest_seat_id


def part2():
    seat_rows, seat_cols = generate_rows_cols()
    num_rows = 128
    num_cols = 8
    all_seat_ids = [[row * num_cols + col for col in range(num_cols)]
                    for row in range(num_rows)]

    for row, col in zip(seat_rows, seat_cols):
        all_seat_ids[row][col] = 0

    missing_seat, is_seat_found = 0, False
    for row in range(num_rows):
        for col in range(num_cols):
            non_empty_seat = all_seat_ids[row][col] != 0
            empty_above = row - 1 >= 0 and all_seat_ids[row-1][col] == 0
            empty_right = col + 1 < num_cols and all_seat_ids[row][col+1] == 0
            empty_below = row + 1 < num_rows and all_seat_ids[row+1][col] == 0
            empty_left = col - 1 >= 0 and all_seat_ids[row][col-1] == 0

            if all([non_empty_seat, empty_above, empty_right, empty_below, empty_left]):
                missing_seat = row * num_cols + col
                is_seat_found = True
                break

        if is_seat_found:
            break

    return missing_seat


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
