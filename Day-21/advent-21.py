"""
URL for challenge: https://adventofcode.com/2020/day/21

Check PR description for working of solution.
"""


import matplotlib.pyplot as plt
from networkx import draw
from networkx import Graph
from networkx.algorithms.bipartite import maximum_matching
from networkx.drawing.layout import bipartite_layout


def process_input():
    f = open("advent-21-input.txt")
    ingr_appearances, allergen_prospects = {}, {}
    for line in f.readlines():
        ingredients, allergens = line.strip().split(' (contains ')
        ingredients = set(ingredients.split(' '))
        allergens = allergens.strip(')').split(', ')

        for allrg in allergens:
            if allrg not in allergen_prospects:
                allergen_prospects[allrg] = ingredients
            else:
                allergen_prospects[allrg] = allergen_prospects[allrg].intersection(
                    ingredients)

        for ingr in ingredients:
            if ingr not in ingr_appearances:
                ingr_appearances[ingr] = 1
            else:
                ingr_appearances[ingr] += 1

    return ingr_appearances, allergen_prospects


def part1():
    ingr_appearances, allergen_prospects = process_input()
    mm_edges = maximum_matching(Graph(allergen_prospects))
    ingr_without_allergens = ingr_appearances.keys() - (mm_edges.keys() - allergen_prospects.keys())

    return sum([ingr_appearances[ingr] for ingr in ingr_without_allergens])


def part2():
    _, allergen_prospects = process_input()
    mm_edges = maximum_matching(Graph(allergen_prospects))
    ingr_with_allergens = [mm_edges[allergen] for allergen in allergen_prospects]

    return ','.join(sorted(ingr_with_allergens, key=lambda x: mm_edges[x]))


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
         labels={node: node for node in graph.nodes}, node_size=600, node_color="green")


run()
