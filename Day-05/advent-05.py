"""
URL for challenge: https://adventofcode.com/2020/day/5
"""

def part1():
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

    highest_seat_id = 0
    for row, col in zip(seat_rows, seat_cols):
        seat_id = row * 8 + col
        if seat_id > highest_seat_id:
            highest_seat_id = seat_id

    return highest_seat_id

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
