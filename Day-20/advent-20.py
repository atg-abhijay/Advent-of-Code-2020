"""
URL for challenge: https://adventofcode.com/2020/day/20
"""


from itertools import combinations
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import maximum_flow
from networkx.drawing import multipartite_layout
from tqdm import tqdm


def process_input():
    f = open("advent-20-input.txt")
    tiles, current_tile_id = {}, 0

    for line in f.readlines():
        line = line.strip()
        if "Tile" in line:
            current_tile_id = int(line.split("Tile ")[1][:-1])
            image = []
        elif line:
            image.append(line.replace('.', '0').replace('#', '1'))
        else:
            tiles[current_tile_id] = image

    tiles[current_tile_id] = image

    for tile_id, image in tiles.items():
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

        tiles[tile_id] = borders

    return tiles


def part1():
    tiles = process_input()
    flow_network = nx.DiGraph(
        [(tile_id, 'sink', {'capacity': 4}) for tile_id in tiles])

    flow_network.add_node('source', layer=0)
    flow_network.nodes['sink']['layer'] = 5
    for tile_id in tiles:
        flow_network.nodes[tile_id]['layer'] = 4

    for u, v in tqdm(combinations(tiles.keys(), 2)):
        is_connection = False
        for u_pos, u_border in tiles[u].items():
            for v_pos, v_border in tiles[v].items():
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

    _, flow_dict = maximum_flow(flow_network, 'source', 'sink')

    # Draw the flow network with capacities and flow amounts
    # draw_flow_network(flow_network, "Capacities")
    # draw_flow_network(flow_network, "Flow amounts", flow_dict)

    # print(flow_network.in_degree(nbunch=[
    #       node for node, data in flow_network.nodes(data=True) if data['layer'] == 3]))

    result = 1
    for tile_id, flow in flow_dict.items():
        if 'sink' in flow and flow['sink'] == 2:
            result *= tile_id

    return result


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

    plt.show()


def draw_flow_network(graph, title, flow_dict=None):
    plt.figure(num=title)
    positions = multipartite_layout(graph, subset_key='layer')
    nx.draw(graph, pos=positions, labels={
            node: node for node in graph.nodes}, node_size=600, node_color="green")

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