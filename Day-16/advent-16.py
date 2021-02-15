"""
URL for challenge: https://adventofcode.com/2020/day/16
"""


def process_input():
    f = open("advent-16-input.txt")
    # (k, v) = (field name, (mathematical) set of valid values)
    ticket_fields = {}
    puzzle_input = f.readlines()
    current_idx = 0
    # Parse ticket fields
    for idx, line in enumerate(puzzle_input):
        current_idx = idx
        if line == '\n':
            break

        field = line.strip().split(': ')
        ranges = field[1].split(' or ')
        field_ranges = set()
        for r in ranges:
            r = r.split('-')
            r = set(range(int(r[0]), int(r[1]) + 1))
            field_ranges = field_ranges.union(r)

        ticket_fields[field[0]] = field_ranges

    # Parse my ticket
    current_idx += 2
    my_ticket = puzzle_input[current_idx].strip().split(',')
    my_ticket = [int(x) for x in my_ticket]

    # Parse nearby tickets
    current_idx += 3
    nearby_tickets = []
    for line in puzzle_input[current_idx:]:
        ticket = [int(x) for x in line.strip().split(',')]
        nearby_tickets.append(ticket)

    return ticket_fields, my_ticket, nearby_tickets


def part1():
    ticket_fields, _, nearby_tickets = process_input()
    # Create a set that contains the union of
    # the valid values for all of the fields
    all_valid_vals = set()
    for valid_range in ticket_fields.values():
        all_valid_vals = all_valid_vals.union(valid_range)

    invalid_vals_sum = 0
    for ticket in nearby_tickets:
        invalid_vals_sum += is_ticket_valid(ticket, all_valid_vals)[1]

    return invalid_vals_sum


def is_ticket_valid(ticket, all_valid_vals):
    invalid_vals = set(ticket).difference(all_valid_vals)
    if not invalid_vals:
        return True, 0

    elif len(invalid_vals) == 1:
        return False, invalid_vals.pop()

    else:
        print("More than one invalid value!")
        exit(1)








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
