"""
URL for challenge: https://adventofcode.com/2020/day/16

Check PR description for notes on solution.
"""

from itertools import product
import matplotlib.pyplot as plt
from networkx import draw
from networkx import Graph
from networkx.drawing.layout import bipartite_layout
from networkx.algorithms.bipartite import maximum_matching


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

    graph = build_bipartite_graph(valid_tickets, ticket_fields)
    departures_product = 1
    mm_edges = maximum_matching(graph).items()
    for start_edge, end_edge in mm_edges:
        if isinstance(start_edge, str) and "departure" in start_edge:
            departures_product *= my_ticket[end_edge]

    # Uncomment the following to draw the graphs -
    # draw_bipartite_graph(graph, ticket_fields.keys())
    # draw_bipartite_graph(Graph(mm_edges), ticket_fields.keys())

    return departures_product


def build_bipartite_graph(valid_tickets, ticket_fields):
    graph, num_columns = Graph(), len(valid_tickets[0])
    for column_idx, field in product(range(num_columns), ticket_fields):
        column_values = {ticket[column_idx] for ticket in valid_tickets}
        if column_values.issubset(ticket_fields[field]):
            graph.add_edge(field, column_idx)

    return graph


def run():
    chall = int(input("Please enter either 1 or 2 for the challenges: "))
    if chall == 1:
        print(part1())
    elif chall == 2:
        print(part2())
    else:
        print("You need to enter either 1 or 2")
        exit(1)

    plt.show()


def draw_bipartite_graph(graph, first_partition_nodes):
    plt.figure()
    draw(graph, pos=bipartite_layout(graph, first_partition_nodes),
         labels={node: node for node in graph}, node_size=600, node_color="green")


run()
