"""
URL for challenge: https://adventofcode.com/2020/day/20
"""


from itertools import combinations
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import maximum_flow
from networkx.algorithms.flow import preflow_push
from networkx.drawing import multipartite_layout
from tqdm import tqdm


def process_input():
    f = open("/Users/AbhijayGupta/Projects/Advent-of-Code-2020/Day-20/advent-20-input.txt")
    tiles, current_tile_id = {}, 0

    for line in f.readlines():
        line = line.strip()
        if "Tile" in line:
            current_tile_id = int(line.split("Tile ")[1][:-1])
            image = []
        elif line:
            image.append(line.replace('.', '0').replace('#', '1'))
        else:
            tiles[current_tile_id] = {"image": image}

    tiles[current_tile_id] = {"image": image}

    for tile_id, image_dict in tiles.items():
        image = image_dict["image"]
        borders = {"top": int(image[0], 2)}
        left_border, right_border = [], []
        for row in image:
            right_border.append(row[-1])
            left_border.append(row[0])

        borders["right"] = int(''.join(right_border), 2)
        borders["left"] = int(''.join(left_border), 2)
        borders["bottom"] = int(image[-1], 2)

        # Append reverse versions of borders
        borders["top_rev"] = int(image[0][::-1], 2)
        borders["right_rev"] = int(''.join(reversed(right_border)), 2)
        borders["left_rev"] = int(''.join(reversed(left_border)), 2)
        borders["bottom_rev"] = int(image[-1][::-1], 2)

        tiles[tile_id]["borders"] = borders

    return tiles


def build_flow_network():
    tiles = process_input()
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

                flow_network.add_edges_from([(u_label, u), (v_label, v)], capacity=1)
                flow_network.nodes[u_label]['layer'] = 3
                flow_network.nodes[v_label]['layer'] = 3

        if is_connection:
            flow_network.add_edge('source', (u, v), capacity=2)
            flow_network.nodes[(u, v)]['layer'] = 1

    return flow_network


def part1():
    flow_network = build_flow_network()
    residual_graph = preflow_push(flow_network, 'source', 'sink')
    _, flow_dict = maximum_flow(flow_network, 'source', 'sink')

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
    flow_network = build_flow_network()
    _, flow_dict = maximum_flow(flow_network, 'source', 'sink')
    # R = preflow_push(flow_network, 'source', 'sink')
    for tile in flow_network.predecessors('sink'):
        if flow_dict[tile]['sink'] == 2:
            corner_tile = tile
            break

    tile_neighbours = {}
    queue = [corner_tile]
    while queue:
        tile = queue.pop()
        if tile in tile_neighbours:
            continue

        tile_neighbours[tile] = []
        for side in flow_network.predecessors(tile):
            if flow_dict[side][tile] == 1:
                uv_config = next(flow_network.predecessors(side))
                for v in flow_network.successors(uv_config):
                    if v != side:
                        tile_neighbours[tile].append((side, v))
                        queue.append(int(v.split('_')[0]))

    # print(tile_neighbours)
    remove_image_borders()

    # queue = tile_neighbours[corner_tile]
    # full_image = [[]]

    # while queue:
    #     start_tile, end_tile = queue.pop()
    #     start_tile_id = int(start_tile.split('_')[0])
    #     full_image[-1].append(start_tile_id)
    #     end_tile_id, end_tile_dirn = end_tile.split('_', 1)
    #     end_tile_id = int(end_tile_id)
    #     full_image[-1].append(end_tile_id)

    #     end_tile_nbrs = tile_neighbours[end_tile_id]
    #     while 1:
    #         if "top" in end_tile_dirn:




    # while queue:
    #     tile = queue.pop()
    #     full_image.append([tile])
    #     tile_nbrs = tile_neighbours[tile]
    #     while tile_nbrs:
    #         start_tile, end_tile = tile_nbrs.pop()
    #         nbr, nbr_side = end_tile.split('_', 1)
    #         nbr = int(nbr)
    #         full_image[-1].append(nbr)
    #         temp = [nbr]
    #         while temp:






    return


def remove_image_borders():
    tiles = process_input()
    for values_dict in tiles.values():
        image = values_dict["image"]
        image.pop(0)
        image.pop()
        for idx, row in enumerate(image):
            image[idx] = row[1:-1]

    return


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
