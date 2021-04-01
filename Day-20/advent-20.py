"""
URL for challenge: https://adventofcode.com/2020/day/20
"""


from itertools import combinations
from itertools import chain
from itertools import tee
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import maximum_flow
from networkx.drawing import multipartite_layout
import numpy as np
from tqdm import tqdm


def process_input():
    f = open(
        "/Users/AbhijayGupta/Projects/Advent-of-Code-2020/Day-20/advent-20-input.txt")
    tiles, current_tile_id = {}, 0

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

    for tile_id, image_dict in tiles.items():
        image = image_dict["image"]
        borders = {"top": int(''.join(image[0]), 2)}
        left_border, right_border = [], []
        for row in image:
            right_border.append(row[-1])
            left_border.append(row[0])

        borders["right"] = int(''.join(right_border), 2)
        borders["left"] = int(''.join(left_border), 2)
        borders["bottom"] = int(''.join(image[-1]), 2)

        # Append reverse versions of borders
        borders["top_rev"] = int(''.join(image[0][::-1]), 2)
        borders["right_rev"] = int(''.join(reversed(right_border)), 2)
        borders["left_rev"] = int(''.join(reversed(left_border)), 2)
        borders["bottom_rev"] = int(''.join(image[-1][::-1]), 2)

        tiles[tile_id]["borders"] = borders

    return tiles


def build_flow_network(tiles):
    flow_network = nx.DiGraph(
        [(tile_id, 'sink', {'capacity': 4}) for tile_id in tiles])

    flow_network.add_node('source', layer=0)
    flow_network.nodes['sink']['layer'] = 5
    for tile_id in tiles:
        flow_network.nodes[tile_id]['layer'] = 4

    for u, v in tqdm(combinations(tiles.keys(), 2)):
        is_connection = False
        for u_pos, u_border in tiles[u]["borders"].items():
            for v_pos, v_border in tiles[v]["borders"].items():
                u_label, v_label = f'{u}_{u_pos}', f'{v}_{v_pos}'
                uv_label = '_'.join([u_label, v_label])
                if u_border ^ v_border == 0:
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
    tiles = process_input()
    flow_network = build_flow_network(tiles)
    _, flow_dict = maximum_flow(flow_network, 'source', 'sink')

    # print(flow_network.edges(data=True))

    # Draw the flow network with capacities and flow amounts
    # draw_flow_network(flow_network, "Capacities")
    # draw_flow_network(residual_graph, "Residual Graph")
    # draw_flow_network(flow_network, "Flow amounts", flow_dict)

    # layer_nodes = [node for node, data in flow_network.nodes(data=True) if data['layer'] == 1]
    # in_degrees = set()
    # print("#Nodes in layer:", len(layer_nodes))
    # for _, value in flow_network.in_degree(nbunch=layer_nodes):
    #     in_degrees.add(value)

    # print(in_degrees)

    # print("#Nodes:", flow_network.number_of_nodes())
    # print("#Edges:", flow_network.number_of_edges())

    result = 1
    for tile_id, flow in flow_dict.items():
        if 'sink' in flow and flow['sink'] == 2:
            result *= tile_id

    return result


def part2():
    tiles = process_input()
    flow_network = build_flow_network(tiles)
    _, flow_dict = maximum_flow(flow_network, 'source', 'sink')
    for tile in flow_network.predecessors('sink'):
        if flow_dict[tile]['sink'] == 2:
            corner_tile = tile
            break

    tile_conns = generate_tile_connections(
        flow_network, flow_dict, corner_tile)
    conns_copy = tile_conns.copy()
    image_layout = generate_image_layout(tile_conns, corner_tile)
    remove_image_borders(tiles)
    full_image = generate_full_image(conns_copy, tiles, image_layout)
    # print(edges)
    # for e in conns_copy.edges(data=True):
    #     print(e)
    # for e in edges:
    #     print(e)
    for row in image_layout:
        print(row)

    # for row in full_image:
    #     print(row)

    return


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

            uv_config = next(flow_network.predecessors(side))
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


def remove_image_borders(tiles):
    for values_dict in tiles.values():
        image = values_dict["image"]
        image.pop()
        image.pop(0)
        for idx, row in enumerate(image):
            image[idx] = row[1:-1]


def generate_full_image(tile_conns, tiles, image_layout):
    full_image = []
    for row in image_layout:
        image_row = []
        first_itr, second_itr = tee(row)
        next(second_itr)
        for first_tile, second_tile in zip(first_itr, second_itr):
            edge_ends = list(tile_conns[first_tile][second_tile].values())
            tile_side = edge_ends[0] if str(first_tile) in edge_ends[0] else edge_ends[1]
            image_row.append(rotate_tile(tiles[first_tile]["image"], tile_side))

        tile_side = edge_ends[0] if str(second_tile) in edge_ends[0] else edge_ends[1]
        image_row.append(np.fliplr(rotate_tile(tiles[second_tile]["image"], tile_side)).tolist())

        for elements in zip(*image_row):
            full_image.append(list(chain(*elements)))

    return full_image


def rotate_tile(tile_image, tile_side):
    tile_side = tile_side.split('_', 1)[1]

    if "top" in tile_side:
        tile_image = np.rot90(tile_image, axes=(1, 0))
    elif "left" in tile_side:
        tile_image = np.fliplr(tile_image)
    elif "bottom" in tile_side:
        tile_image = np.transpose(tile_image)

    if "rev" in tile_side:
        tile_image = np.flipud(tile_image)

    return tile_image.tolist()


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
    positions = multipartite_layout(graph, subset_key='layer')
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
