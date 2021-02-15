"""
URL for challenge: https://adventofcode.com/2020/day/16

Check PR description for notes on solution.
"""


class Row(object):
    """
    Store the fit of all values in a specific
    ticket column against each of the ticket fields
    """
    def __init__(self, elements, ticket_column):
        self.elements = elements
        self.ticket_column = ticket_column


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
    all_valid_vals = set.union(*ticket_fields.values())

    invalid_vals_sum = 0
    for ticket in nearby_tickets:
        invalid_vals_sum += is_ticket_valid(ticket, all_valid_vals)[1]

    return invalid_vals_sum


def is_ticket_valid(ticket, all_valid_vals):
    invalid_vals = set(ticket).difference(all_valid_vals)
    if invalid_vals:
        return False, sum(invalid_vals)

    return True, 0


def part2():
    ticket_fields, my_ticket, nearby_tickets = process_input()
    # Create a set that contains the union of
    # the valid values for all of the fields
    all_valid_vals = set.union(*ticket_fields.values())
    valid_tickets = [t for t in nearby_tickets if is_ticket_valid(t, all_valid_vals)[0]]

    matrix, fields = [], list(ticket_fields.keys())

    # Build a matrix where xth row represents fit
    # of xth column (values from all valid tickets
    # at that column) against each of the fields
    for column_idx in range(len(valid_tickets[0])):
        column_values = {ticket[column_idx] for ticket in valid_tickets}
        field_fits = []
        for field in fields:
            if column_values.issubset(ticket_fields[field]):
                field_fits.append(1)
            else:
                field_fits.append(0)

        matrix.append(Row(field_fits, column_idx))

    # print_matrix(matrix, "Original matrix - ")

    # Sort the matrix such that the rows with
    # the least number of 1s appear at the top
    matrix.sort(key=lambda x: sum(x.elements))
    # print_matrix(matrix, "Sorted matrix - ")

    for row_idx in range(len(matrix)):
        simplify_row(matrix, row_idx)

    # print_matrix(matrix, "After simplification - ")
    output = 1
    for idx, field in enumerate(fields):
        if "departure" not in field:
            continue

        for row in matrix:
            if row.elements[idx]:
                # print(field, ':')
                # print("- Ticket column:", row.ticket_column)
                # print("- Value in my ticket:", my_ticket[row.ticket_column])
                output *= my_ticket[row.ticket_column]
                break

    return output


def simplify_row(matrix, row_idx):
    # Find the first non-zero entry in the
    # target row. Store it's value and index.
    target_row = matrix[row_idx].elements
    non_zero, non_zero_idx = -1, -1
    for idx, entry in enumerate(target_row):
        if entry:
            non_zero = entry
            non_zero_idx = idx
            break

    # If there are no non-zero entries, no
    # modifications have to be made to this row.
    if non_zero_idx == -1:
        return

    # Make every entry above and
    # below the leading 1 to be zero
    tolerance = 0.0000001
    for i, row_obj in enumerate(matrix):
        row = row_obj.elements
        if i == row_idx:
            continue

        coefficient = -1 * row[non_zero_idx] / non_zero
        if not coefficient:
            continue

        for j, entry in enumerate(row):
            new_value = row[j] + coefficient * target_row[j]
            if abs(new_value) < tolerance:
                row[j] = 0
            else:
                row[j] = new_value

    # Divide each entry by the leading entry
    # so that the leading entry becomes 1.
    if non_zero != 1:
        matrix[row_idx].elements = [entry*(1/non_zero) for entry in target_row]


def run():
    chall = int(input("Please enter either 1 or 2 for the challenges: "))
    if chall == 1:
        print(part1())
    elif chall == 2:
        print(part2())
    else:
        print("You need to enter either 1 or 2")
        exit(1)


def print_matrix(matrix, message):
    print(message)

    for row in matrix:
        elements = [int(x) for x in row.elements]
        print(elements, "Sum:", sum(elements), "\t", "Ticket column:", row.ticket_column)

    print()


run()
