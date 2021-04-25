"""
URL for challenge: https://adventofcode.com/2020/day/20
"""


import itertools as it
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from tqdm import tqdm


def process_input():
    f = open(
        "/Users/AbhijayGupta/Projects/Advent-of-Code-2020/Day-20/advent-20-input.txt")
    tiles, current_tile_id = {}, 0

    # Parse images of the tiles
    for line in f.readlines():
        line = line.strip()
        if "Tile" in line:
            current_tile_id = int(line.split("Tile ")[1][:-1])
            image = []
        elif line:
            image.append(list(line.replace('.', '0').replace('#', '1')))
        else:
            tiles[current_tile_id] = {"image": image}

    tiles[current_tile_id] = {"image": image}

    # Determine borders of the tiles
    for tile_id, image_dict in tiles.items():
        image = image_dict["image"]
        borders = {
            "top": ''.join(image[0]),
            "right": ''.join([row[-1] for row in image]),
            "bottom": ''.join(image[-1]),
            "left": ''.join([row[0] for row in image])
        }

        # Append reverse versions of borders
        for pos in ["top", "right", "left", "bottom"]:
            borders[pos + "_rev"] = borders[pos][::-1]

        tiles[tile_id]["borders"] = borders

    return tiles


def build_flow_network(tiles):
    flow_network = nx.DiGraph(
        [(tile_id, 'sink', {'capacity': 4}) for tile_id in tiles])

    flow_network.add_node('source', layer=0)
    flow_network.nodes['sink']['layer'] = 5
    for tile_id in tiles:
        flow_network.nodes[tile_id]['layer'] = 4

    for u, v in tqdm(it.combinations(tiles.keys(), 2)):
        is_connection = False
        for u_pos, u_border in tiles[u]["borders"].items():
            for v_pos, v_border in tiles[v]["borders"].items():
                u_label, v_label = f'{u}_{u_pos}', f'{v}_{v_pos}'
                uv_label = '_'.join([u_label, v_label])
                if u_border == v_border:
                    is_connection = True
                    flow_network.add_edges_from(
                        [((u, v), uv_label), (uv_label, u_label), (uv_label, v_label)])
                    flow_network.nodes[uv_label]['layer'] = 2

                flow_network.add_edges_from(
                    [(u_label, u), (v_label, v)], capacity=1)
                flow_network.nodes[u_label]['layer'] = 3
                flow_network.nodes[v_label]['layer'] = 3

        if is_connection:
            flow_network.add_edge('source', (u, v), capacity=2)
            flow_network.nodes[(u, v)]['layer'] = 1

    return flow_network


def part1():
    flow_network = build_flow_network(process_input())
    _, flow_dict = nx.maximum_flow(flow_network, 'source', 'sink')

    # Draw the flow network with capacities and flow amounts
    # draw_flow_network(flow_network, "Capacities")
    # draw_flow_network(flow_network, "Flow amounts", flow_dict)

    result = 1
    for tile_id, flow in flow_dict.items():
        if 'sink' in flow and flow['sink'] == 2:
            result *= tile_id

    return result


def part2():
    tiles = process_input()
    flow_network = build_flow_network(tiles)
    _, flow_dict = nx.maximum_flow(flow_network, 'source', 'sink')
    for tile in flow_network.predecessors('sink'):
        if flow_dict[tile]['sink'] == 2:
            corner_tile = tile
            break

    tile_conns = generate_tile_connections(
        flow_network, flow_dict, corner_tile)
    conns_copy = tile_conns.copy()
    image_layout = generate_image_layout(tile_conns, corner_tile)
    for row in image_layout:
        print(row)

    full_image = create_full_image(conns_copy, tiles, image_layout)
    sea_monster = process_sea_monster()
    arrangements = [sea_monster, np.flipud(sea_monster)]
    for num_rots in range(1, 4):
        arrangements.append(np.rot90(sea_monster, k=num_rots))
        arrangements.append(np.flipud(arrangements[-1]))

    corner_x, corner_y = 0, 0
    image_height, image_width = len(full_image), len(full_image[0])
    num_sea_monsters = 0
    for idx, arrng in enumerate(arrangements):
        height, width = len(arrng), len(arrng[0])
        for corner_y in range(image_height):
            for corner_x in range(image_width):
                image_chunk = []
                width_bound = corner_x + width < image_width + 1
                height_bound = corner_y + height < image_height + 1
                if width_bound and height_bound:
                    for hgt in range(height):
                        image_chunk.append(full_image[corner_y+hgt][corner_x:corner_x+width])

                    bin_monster = int(''.join(it.chain(*arrng)), 2)
                    bin_chunk = int(''.join(it.chain(*image_chunk)), 2)

                    if bin_monster & bin_chunk == bin_monster:
                        num_sea_monsters += 1

        if num_sea_monsters:
            break

    eval_roughness = lambda grid: sum([list(row).count('1') for row in grid])
    total_roughness = eval_roughness(full_image)
    monsters_roughness = eval_roughness(sea_monster) * num_sea_monsters

    # Draw the flow network with capacities and flow amounts
    # draw_flow_network(flow_network, "Capacities")
    # draw_flow_network(flow_network, "Flow amounts", flow_dict)

    print(total_roughness, monsters_roughness)
    print("Arrangement #:", idx)
    return total_roughness - monsters_roughness


def generate_tile_connections(flow_network, flow_dict, corner_tile):
    tile_conns = nx.Graph()
    tile_conns.add_node(corner_tile, visited=False)
    nodes = tile_conns.nodes
    queue = [corner_tile]
    while queue:
        tile = queue.pop()
        if 'visited' in nodes[tile] and nodes[tile]['visited']:
            continue

        for side in flow_network.predecessors(tile):
            if flow_dict[side][tile] != 1:
                continue

            while 1:
                uv_config = next(flow_network.predecessors(side))
                if flow_dict[uv_config][side] == 1:
                    break

            for v_tile_side in flow_network.successors(uv_config):
                if v_tile_side == side:
                    continue

                v_tile_id = int(v_tile_side.split('_')[0])
                tile_conns.add_edge(
                    tile, v_tile_id, end_A=side, end_B=v_tile_side)
                queue.append(v_tile_id)

        nodes[tile]['visited'] = True

    return tile_conns


def generate_image_layout(tile_conns, corner_tile):
    for tile in tile_conns:
        tile_conns.nodes[tile]['weight'] = tile_conns.degree[tile]

    queue, image_layout = [corner_tile], [[]]
    counter, at_row_head = 0, True
    width = len(tile_conns.nodes) ** 0.5
    while queue:
        tile = queue.pop()
        image_layout[-1].append(tile)
        counter += 1
        # Reached the end of the row
        if counter == width:
            # Reached the end of the grid
            if not tile_conns[tile]:
                continue

            nbr = next(tile_conns.neighbors(tile))
            tile_conns.remove_edge(tile, nbr)
            for node in [tile, nbr]:
                tile_conns.nodes[node]['weight'] -= 5

            image_layout.append([])
            counter, at_row_head = 0, True
            continue

        next_in_row = min(tile_conns[tile],
                          key=lambda x: tile_conns.nodes[x]['weight'])

        if at_row_head:
            if len(tile_conns[tile]) != 1:
                next_row_head = set(tile_conns[tile]).difference(
                    {next_in_row}).pop()
                queue.append(next_row_head)
                tile_conns.remove_edge(tile, next_row_head)
                for node in [tile, next_row_head]:
                    tile_conns.nodes[node]['weight'] -= 5

            queue.append(next_in_row)
            tile_conns.remove_edge(tile, next_in_row)
            tile_conns.nodes[next_in_row]['weight'] -= 5
            at_row_head = False

        else:
            queue.append(next_in_row)
            for nbr in list(tile_conns[tile]):
                tile_conns.nodes[nbr]['weight'] -= 5
                tile_conns.remove_edge(tile, nbr)

    return image_layout


def remove_image_borders(full_image):
    for image_row in full_image:
        for i, tile in enumerate(image_row):
            tile = tile[1:-1]
            for j, row in enumerate(tile):
                tile[j] = row[1:-1]

            image_row[i] = tile


def orient_corner_tile(tile_conns, image_layout):
    corner_tile = image_layout[0][0]
    orientations = {
        ('top', 'right'): ('', '_rev'),
        ('right', 'bottom'): ('', ''),
        ('bottom', 'left'): ('_rev', ''),
        ('left', 'top'): ('_rev', '_rev')
    }
    right_nbr, bottom_nbr = image_layout[0][1], image_layout[1][0]
    get_side = lambda nbr: next(filter(lambda side: str(corner_tile) in side,
                                       tile_conns[corner_tile][nbr].values())).split('_')[1]

    active_sides = (get_side(right_nbr), get_side(bottom_nbr))
    for sides, ortns in orientations.items():
        if active_sides == sides:
            new_sides = [s + o for s, o in zip(sides, ortns)]
            break

        elif active_sides == tuple(reversed(sides)):
            new_sides = [s + o for s, o in zip(reversed(sides), reversed(ortns))]
            break

    for new_side, nbr in zip(new_sides, [right_nbr, bottom_nbr]):
        new_side = str(corner_tile) + '_' + new_side
        edge_ends = list(tile_conns[corner_tile][nbr].values())
        if str(corner_tile) in edge_ends[0]:
            old_side, nbr_side = edge_ends[0], edge_ends[1]
        else:
            old_side, nbr_side = edge_ends[1], edge_ends[0]

        if new_side != old_side:
            nbr_side = nbr_side[:-4] if "rev" in nbr_side else nbr_side + "_rev"
            tile_conns.add_edge(corner_tile, nbr, end_A=new_side, end_B=nbr_side)


def create_full_image(tile_conns, tiles, image_layout):
    opposite_sides = nx.Graph([
        ("top", "bottom"), ("top_rev", "bottom_rev"),
        ("right", "left"), ("right_rev", "left_rev")
    ])
    full_image, next_ortn = [], None

    orient_corner_tile(tile_conns, image_layout)

    # Append first row
    image_row = []
    first_itr, second_itr = it.tee(image_layout[0])
    next(second_itr)
    for u_tile, v_tile in zip(first_itr, second_itr):
        edge_ends = list(tile_conns[u_tile][v_tile].values())
        if str(u_tile) in edge_ends[0]:
            u_side, v_side = [ee.split('_', 1)[1] for ee in edge_ends]
        else:
            v_side, u_side = [ee.split('_', 1)[1] for ee in edge_ends]

        target_side = next_ortn if next_ortn else u_side
        image_row.append(rotate_tile(tiles[u_tile]["image"], target_side))
        if target_side != u_side:
            v_side = v_side[:-4] if "rev" in v_side else v_side + "_rev"

        next_ortn = next(opposite_sides.neighbors(v_side))

    image_row.append(rotate_tile(tiles[v_tile]["image"], next_ortn))
    full_image.append(image_row)

    # Add the rest of the rows of the image
    row_idx = 1
    for row in image_layout[1:]:
        image_row = []
        for col_idx, tile_id in enumerate(row):
            north_nbr_border = ''.join(full_image[row_idx-1][col_idx][-1])
            for pos, border in tiles[tile_id]["borders"].items():
                if border == north_nbr_border:
                    image_row.append(np.rot90(rotate_tile(tiles[tile_id]["image"], pos)).tolist())
                    break

        full_image.append(image_row)
        row_idx += 1

    remove_image_borders(full_image)

    final_image = []
    for image_row in full_image:
        for elements in zip(*image_row):
            final_image.append(list(it.chain(*elements)))

    return final_image


def rotate_tile(tile_image, tile_side):
    """
    Rotate tile such that tile_side
    is situated on the right side
    """
    if tile_side == "right":
        return tile_image

    if "top" in tile_side:
        tile_image = np.rot90(tile_image, axes=(1, 0))
    elif "left" in tile_side:
        tile_image = np.fliplr(tile_image)
    elif "bottom" in tile_side:
        tile_image = np.transpose(tile_image)

    if "rev" in tile_side:
        tile_image = np.flipud(tile_image)

    return tile_image.tolist()


def process_sea_monster():
    f = open("/Users/AbhijayGupta/Projects/Advent-of-Code-2020/Day-20/sea-monster.txt")
    return [list(line.strip('\n').replace(' ', '0').replace('#', '1'))
            for line in f.readlines()]


def run():
    # chall = int(input("Please enter either 1 or 2 for the challenges: "))
    chall = 2
    if chall == 1:
        print(part1())
    elif chall == 2:
        print(part2())
    else:
        print("You need to enter either 1 or 2")
        exit(1)

    plt.show()


def draw_flow_network(graph, title, flow_dict=None):
    plt.figure(num=title)
    positions = nx.multipartite_layout(graph, subset_key='layer')
    nx.draw(graph, pos=positions, node_color="green", node_size=600,
            labels={node: node for node in graph})

    # Draw with flow amounts
    if flow_dict:
        tuple_flows = {}
        for tile_id, flow in flow_dict.items():
            for end_edge, flow_amount in flow.items():
                tuple_flows[(tile_id, end_edge)] = flow_amount

        nx.draw_networkx_edge_labels(
            graph, pos=positions, edge_labels=tuple_flows)

    # Draw with capacities
    else:
        nx.draw_networkx_edge_labels(
            graph, pos=positions, edge_labels=nx.get_edge_attributes(graph, 'capacity'))


run()
