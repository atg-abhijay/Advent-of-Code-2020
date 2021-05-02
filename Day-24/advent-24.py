"""
URL for challenge: https://adventofcode.com/2020/day/24

Check PR description for notes on solution.
"""


from tqdm import trange


def process_input():
    f = open("advent-24-input.txt")
    tiles = {(0, 0): 0}
    increments = {
        'e': 2, 'ne': (1, 1), 'se': (1, -1),
        'w': -2, 'nw': (-1, 1), 'sw': (-1, -1)
    }

    for line in f.readlines():
        line = line.strip()
        current_x, current_y = 0, 0
        step, is_north_south = '', False
        for char in line:
            if char in ['n', 's']:
                step, is_north_south = char, True
            else:
                if is_north_south:
                    incr = increments[step + char]
                    current_x += incr[0]
                    current_y += incr[1]
                    step, is_north_south = '', False
                else:
                    current_x += increments[char]

        location = (current_x, current_y)
        if location not in tiles:
            tiles[location] = 1
        else:
            tiles[location] = 1 - tiles[location]

    return tiles


def part1():
    return sum(process_input().values())


def part2():
    # Takes about 10 seconds to run
    tiles = process_input()
    tiles_to_flip, num_days = [], 100
    for _ in trange(num_days):
        tiles = expand_floor(tiles)
        for tile, color in tiles.items():
            num_black_nbs = check_neighbours(tiles, tile)
            # Black
            if color == 1:
                if num_black_nbs == 0 or num_black_nbs > 2:
                    tiles_to_flip.append(tile)
            # White
            else:
                if num_black_nbs == 2:
                    tiles_to_flip.append(tile)

        while tiles_to_flip:
            tile = tiles_to_flip.pop()
            tiles[tile] = 1 - tiles[tile]

    return sum(tiles.values())


def generate_neighbour_locations(target_tile):
    tile_x, tile_y = target_tile
    neigbhour_locations = [(tile_x + x, tile_y + y)
                           for x in [-1, 1] for y in [-1, 1]]
    neigbhour_locations.extend([(tile_x + x, tile_y) for x in [-2, 2]])
    return neigbhour_locations


def expand_floor(tiles):
    tiles_copy = tiles.copy()
    for tile in tiles:
        neighbour_locations = generate_neighbour_locations(tile)
        for nbr in neighbour_locations:
            if nbr not in tiles_copy:
                tiles_copy[nbr] = 0

    return tiles_copy


def check_neighbours(tiles, target_tile):
    num_black_nbs = 0
    neighbour_locations = generate_neighbour_locations(target_tile)
    for nbr in neighbour_locations:
        if nbr in tiles:
            num_black_nbs += tiles[nbr]

    return num_black_nbs


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
