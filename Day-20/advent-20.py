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
    flow_network = build_flow_network()
    _, flow_dict = maximum_flow(flow_network, 'source', 'sink')
    # R = preflow_push(flow_network, 'source', 'sink')
    for tile in flow_network.predecessors('sink'):
        if flow_dict[tile]['sink'] == 2:
            corner_tile = tile
            break

    tile_nbrs = {}
    queue = [corner_tile]
    while queue:
        tile = queue.pop()
        if tile in tile_nbrs:
            continue

        tile_nbrs[tile] = {}
        for side in flow_network.predecessors(tile):
            if flow_dict[side][tile] == 1:
                uv_config = next(flow_network.predecessors(side))
                for v in flow_network.successors(uv_config):
                    if v != side:
                        tile_nbrs[tile][side.split('_', 1)[1]] = v
                        queue.append(int(v.split('_')[0]))

    # print(tile_nbrs)
    remove_image_borders()

    full_image = [[]]
    queue = [corner_tile]
    prev_dirn = ""
    pairs = [("top", "bottom"), ("top_rev", "bottom_rev"),
             ("right", "left"), ("right_rev", "left_rev")]
    while queue:
        tile = queue.pop()
        full_image[-1].append(tile)

        nbrs = tile_nbrs[tile]
        if not prev_dirn:
            _, nbr = nbrs.popitem()

            if nbrs:
                _, nbr2 = nbrs.popitem()
                queue.append(int(nbr2.split('_', 1)[0]))

            nbr_id, nbr_dirn = nbr.split('_', 1)
            queue.append(int(nbr_id))
            prev_dirn = nbr_dirn
        else:
            nbrs.pop(prev_dirn)
            any_valid = False
            for start, end in pairs:
                if prev_dirn == start and end in nbrs:
                    nbr_id, nbr_dirn = nbrs.pop(end).split('_', 1)
                    queue.append(int(nbr_id))
                    prev_dirn = nbr_dirn
                    any_valid = True
                elif prev_dirn == end and start in nbrs:
                    nbr_id, nbr_dirn = nbrs.pop(start).split('_', 1)
                    queue.append(int(nbr_id))
                    prev_dirn = nbr_dirn
                    any_valid = True

            if not any_valid:
                full_image.append([])
                prev_dirn = ""



            # if prev_dirn == "top" and "bottom" in nbrs:
            #     pass
            # elif prev_dirn == "bottom" and "top" in nbrs:
            #     nbr_id, nbr_dirn = nbrs.pop("top").split('_', 1)
            #     queue.append(int(nbr_id))
            #     prev_dirn = nbr_dirn
            # elif prev_dirn == "top_rev" and "bottom_rev" in nbrs:
            #     pass
            # elif prev_dirn == "bottom_rev" and "top_rev" in nbrs:
            #     pass
            # elif prev_dirn == "right" and "left" in nbrs:
            #     pass
            # elif prev_dirn == "left" and "right" in nbrs:
            #     pass
            # elif prev_dirn == "right_rev" and "left_rev" in nbrs:
            #     pass
            # elif prev_dirn == "left_rev" and "right_rev" in nbrs:
            #     pass
            # else:
            #     full_image.append([])
            #     prev_dirn = ""







    # while queue:
    #     nbrs = tile_nbrs[queue.pop()]
    #     for dirn, nbr in nbrs.items():
    #         nbr_id, nbr_dirn = nbr.split('_', 1)
    #         nbr_id = int(nbr_id)

    #         full_image[-1].append(nbr_id)
            # while 1:
                # if nbr_dirn == "top" and "bottom" in tile_nbrs[nbr_id].keys()




    # while queue:
    #     dirn, nbr = queue.pop()
    #     nbr_id, nbr_dirn = nbr.split('_', 1)
    #     image_row_queue = [int(nbr_id)]
    #     while image_row_queue:
    #         tile_id = image_row_queue.pop()
    #         full_image[-1].append(tile_id)
    #         value = ""

    #         pairs = [("top", "bottom")]
            # if "top" in nbr_dirn:
            #     for key in tile_nbrs[tile_id]:
            #         if "bottom" in key:
            #             image_row_queue.append(tile_nbrs[tile_id][])

            #     if "bottom" in tile_nbrs[tile_id]:
            #         value =  tile_nbrs[tile_id][]


    return


def remove_image_borders():
    tiles = process_input()
    for values_dict in tiles.values():
        image = values_dict["image"]
        image.pop()
        image.pop(0)
        for idx, row in enumerate(image):
            image[idx] = row[1:-1]


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
