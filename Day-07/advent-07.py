"""
URL for challenge: https://adventofcode.com/2020/day/7
"""


from collections import deque


class Bag(object):
    """
    Use a deque to expedite popping
    of elements from the left.
    """
    def __init__(self, bag_type):
        self.type = bag_type
        self.children = deque()
        self.parents = deque()
        self.num_children = 0


def process_input():
    """
    Dictionary structure explained in the PR.
    """
    f = open("advent-07-input.txt")
    bags_dict = {}
    for bag_info in f.readlines():
        p_bag_type, children_bags = bag_info.split(sep=' contain ')
        p_bag_type = p_bag_type.split(sep=' bags')[0]
        children_bags = children_bags.split(', ')

        if p_bag_type not in bags_dict:
            parent_obj = Bag(p_bag_type)
            bags_dict[p_bag_type] = parent_obj
        else:
            parent_obj = bags_dict[p_bag_type]

        for c_bag in children_bags:
            if "no other" in c_bag:
                continue

            c_bag = c_bag.split(sep=' ')
            c_bag_type = ' '.join(c_bag[1:3])
            child_bag = {"type": c_bag_type, "quantity": int(c_bag[0])}
            if c_bag_type not in bags_dict:
                child_obj = Bag(c_bag_type)
                child_obj.parents.append(p_bag_type)
                bags_dict[c_bag_type] = child_obj

            else:
                bags_dict[c_bag_type].parents.append(p_bag_type)

            parent_obj.children.append(child_bag)

    return bags_dict


def part1():
    """
    Start with the immediate parents
    of the shiny gold bag and work upwards
    towards the ancestors.
    """
    bags_dict = process_input()
    shiny_gold_bag = bags_dict["shiny gold"]
    parents_deque = shiny_gold_bag.parents
    unique_parents = set()
    while parents_deque:
        p = parents_deque.popleft()
        unique_parents.add(p)
        for q in bags_dict[p].parents:
            parents_deque.append(q)

    return len(unique_parents)


def part2():
    bags_dict = process_input()
    shiny_gold_bag = bags_dict["shiny gold"]
    return find_num_children(shiny_gold_bag, bags_dict)


def find_num_children(bag, bags_dict):
    """
    To avoid incorrect values, check if #children
    are already calculated and return directly.
    A child will contribute itself (hence the +1)
    as well as its own children.
    """
    if bag.num_children:
        return bag.num_children

    for child in bag.children:
        bag.num_children += child["quantity"] * \
            (1 + find_num_children(bags_dict[child["type"]], bags_dict))

    return bag.num_children


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
