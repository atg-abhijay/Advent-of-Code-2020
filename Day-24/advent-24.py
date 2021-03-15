"""
URL for challenge: https://adventofcode.com/2020/day/24
"""


from tqdm import tqdm


def process_input():
    f = open("advent-24-input.txt")
    all_directions = []
    for line in f.readlines():
        line, directions = line.strip(), []
        step, is_north_south = '', False
        for char in line:
            if char in ['n', 's']:
                step, is_north_south = char, True
            else:
                if is_north_south:
                    directions.append(step + char)
                    step, is_north_south = '', False
                else:
                    directions.append(char)

        all_directions.append(directions)

    return all_directions


def part1():
    return sum(map_out_floor().values())


def part2():
    # Takes about 10 seconds to run
    tiles = map_out_floor()
    tiles_to_flip, num_days = [], 100
    for _ in tqdm(range(num_days)):
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


def map_out_floor():
    all_directions = process_input()
    tiles = {(0, 0): 0}
    for directions in all_directions:
        current_x, current_y = 0, 0
        for step in directions:
            if step == 'e':
                current_x += 2
            elif step == 'w':
                current_x -= 2
            elif step == 'se':
                current_x += 1
                current_y -= 1
            elif step == 'sw':
                current_x -= 1
                current_y -= 1
            elif step == 'ne':
                current_x += 1
                current_y += 1
            else:
                current_x -= 1
                current_y += 1

        location = (current_x, current_y)
        if location not in tiles:
            tiles[location] = 1
        else:
            tiles[location] = 1 - tiles[location]

    return tiles


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
        for nb in neighbour_locations:
            if nb not in tiles_copy:
                tiles_copy[nb] = 0

    return tiles_copy


def check_neighbours(tiles, target_tile):
    num_black_nbs = 0
    neighbour_locations = generate_neighbour_locations(target_tile)
    for nb in neighbour_locations:
        if nb in tiles:
            num_black_nbs += tiles[nb]

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
