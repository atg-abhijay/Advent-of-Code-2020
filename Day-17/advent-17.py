"""
URL for challenge: https://adventofcode.com/2020/day/17
"""


from copy import deepcopy


def part1():
    """
    Since all the cubes change their state
    simultaneously, two pocket dimensions
    will be required since the original
    dimension cannot be modified whilst
    the state transitions are happening.
    """
    f = open("advent-17-input.txt")
    pocket_dimn = {0: {}}
    for row_idx, line in enumerate(f.readlines()):
        row_dict = {}
        for col_idx, state in enumerate(line.strip()):
            if state == "#":
                row_dict[col_idx] = 1
            else:
                row_dict[col_idx] = 0

        pocket_dimn[0][row_idx] = row_dict

    # Create a copy dimension to keep
    # track of the state transitions
    pocket_dimn_after = deepcopy(pocket_dimn)

    for i in range(6):
        # The state transitions will occur for the
        # current input AS WELL AS the immediate
        # neighbours. Add those neighbours.
        for z, layer in pocket_dimn.items():
            for x, row in layer.items():
                for y, state in row.items():
                    neighbours = generate_neighbour_locations((z, x, y))
                    add_neighbours_to_dimn(neighbours, pocket_dimn_after)

        # This dimension contains the current input
        # and the immediate neighbours. Apply the
        # state transitions for all of them with
        # respect to the original dimension.
        for z, layer in pocket_dimn_after.items():
            for x, row in layer.items():
                for y, state in row.items():
                    neighbours = generate_neighbour_locations((z, x, y))
                    pocket_dimn_after[z][x][y] = get_new_state(
                        state, neighbours, pocket_dimn)

        # Copy over the modified dimension
        # in preparation for the next iteration
        pocket_dimn = deepcopy(pocket_dimn_after)

    # Determine the number of active cubes
    num_active_cubes = 0
    for z, layer in pocket_dimn.items():
        for x, row in layer.items():
            for y, state in row.items():
                num_active_cubes += state

    return num_active_cubes


def generate_neighbour_locations(target):
    neighbours = [(target[0] + z, target[1] + x, target[2] + y)
                  for z in range(-1, 2) for x in range(-1, 2) for y in range(-1, 2)]
    neighbours.remove(target)
    return neighbours


def add_neighbours_to_dimn(neighbours, pocket_dimn):
    for nb_z, nb_x, nb_y in neighbours:
        if nb_z not in pocket_dimn:
            pocket_dimn[nb_z] = {}

        layer = pocket_dimn[nb_z]
        if nb_x not in layer:
            layer[nb_x] = {}

        row = layer[nb_x]
        if nb_y not in row:
            row[nb_y] = 0


def get_new_state(target_state, neighbours, pocket_dimn):
    num_active_nbs = 0
    for nb_z, nb_x, nb_y in neighbours:
        if nb_z not in pocket_dimn:
            continue

        layer = pocket_dimn[nb_z]
        if nb_x not in layer:
            continue

        row = layer[nb_x]
        if nb_y not in row:
            continue

        num_active_nbs += pocket_dimn[nb_z][nb_x][nb_y]

    if target_state:
        if num_active_nbs < 2 or num_active_nbs > 3:
            return 0
    else:
        if num_active_nbs == 3:
            return 1

    return target_state


def part2():
    f = open("advent-17-input.txt")
    pocket_dimn = {0: {0: {}}}
    for row_idx, line in enumerate(f.readlines()):
        row_dict = {}
        for col_idx, state in enumerate(line.strip()):
            if state == "#":
                row_dict[col_idx] = 1
            else:
                row_dict[col_idx] = 0

        pocket_dimn[0][0][row_idx] = row_dict

    pocket_dimn_after = deepcopy(pocket_dimn)

    for i in range(6):
        for w, hypercube in pocket_dimn.items():
            for z, layer in hypercube.items():
                for x, row in layer.items():
                    for y, state in row.items():
                        neighbours = generate_neighbours((w, z, x, y))
                        add_neighbours(neighbours, pocket_dimn_after)

        for w, hypercube in pocket_dimn_after.items():
            for z, layer in hypercube.items():
                for x, row in layer.items():
                    for y, state in row.items():
                        neighbours = generate_neighbours((w, z, x, y))
                        pocket_dimn_after[w][z][x][y] = find_new_state(
                            state, neighbours, pocket_dimn)

        pocket_dimn = deepcopy(pocket_dimn_after)

    # Determine the number of active cubes
    num_active_cubes = 0
    for w, hypercube in pocket_dimn.items():
        for z, layer in hypercube.items():
            for x, row in layer.items():
                for y, state in row.items():
                    num_active_cubes += state

    return num_active_cubes


def generate_neighbours(target):
    neighbours = [(target[0] + w, target[1] + z, target[2] + x, target[3] + y)
                  for w in range(-1, 2) for z in range(-1, 2) for x in range(-1, 2) for y in range(-1, 2)]
    neighbours.remove(target)
    return neighbours


def add_neighbours(neighbours, pocket_dimn):
    for nb_w, nb_z, nb_x, nb_y in neighbours:
        if nb_w not in pocket_dimn:
            pocket_dimn[nb_w] = {}

        hypercube = pocket_dimn[nb_w]
        if nb_z not in hypercube:
            hypercube[nb_z] = {}

        layer = hypercube[nb_z]
        if nb_x not in layer:
            layer[nb_x] = {}

        row = layer[nb_x]
        if nb_y not in row:
            row[nb_y] = 0


def find_new_state(target_state, neighbours, pocket_dimn):
    num_active_nbs = 0
    for nb_w, nb_z, nb_x, nb_y in neighbours:
        if nb_w not in pocket_dimn:
            continue

        hypercube = pocket_dimn[nb_w]
        if nb_z not in hypercube:
            continue

        layer = hypercube[nb_z]
        if nb_x not in layer:
            continue

        row = layer[nb_x]
        if nb_y not in row:
            continue

        num_active_nbs += pocket_dimn[nb_w][nb_z][nb_x][nb_y]

    if target_state:
        if num_active_nbs < 2 or num_active_nbs > 3:
            return 0
    else:
        if num_active_nbs == 3:
            return 1

    return target_state


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
