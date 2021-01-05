"""
URL for challenge: https://adventofcode.com/2020/day/16
"""


def part1():
    f = open("advent-16-input.txt")
    ticket_fields = {}
    puzzle_input = f.readlines()
    current_idx = 0
    for idx, line in enumerate(puzzle_input):
        current_idx = idx
        if line == '\n':
            break

        field = line.strip().split(': ')
        ranges = field[1].split(' or ')
        field_ranges = []
        for r in ranges:
            r = r.split('-')
            field_ranges.append((int(r[0]), int(r[1])))

        ticket_fields[field[0]] = field_ranges

    current_idx += 2
    my_ticket = puzzle_input[current_idx].strip().split(',')
    my_ticket = [int(x) for x in my_ticket]

    current_idx += 3
    nearby_tickets = []
    for line in puzzle_input[current_idx:]:
        ticket = [int(x) for x in line.strip().split(',')]
        nearby_tickets.append(ticket)


    invalid_vals_sum = 0
    for ticket in nearby_tickets:
        invalid_vals_sum += is_ticket_valid(ticket, ticket_fields)[1]

    return invalid_vals_sum


def is_ticket_valid(ticket, ticket_fields):
    for val in ticket:
        is_val_valid = False
        for first_range, second_range in ticket_fields.values():
            check_a = val > first_range[0] and val <= first_range[1]
            check_b = val > second_range[0] and val <= second_range[1]
            is_val_valid = is_val_valid or check_a or check_b
            if is_val_valid:
                break

        if not is_val_valid:
            return False, val

    return True, 0


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
