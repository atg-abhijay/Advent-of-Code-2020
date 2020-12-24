"""
URL for challenge: https://adventofcode.com/2020/day/7
"""


class Bag(object):
    def __init__(self, bag_type):
        self.type = bag_type
        self.children = []
        self.parents = []


def part1():
    f = open("/Users/AbhijayGupta/Projects/Advent-of-Code-2020/Day-07/advent-07-input.txt")
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


def part2():
    return


def run():
    # chall = int(input("Please enter either 1 or 2 for the challenges: "))
    chall = 1
    if chall == 1:
        print(part1())
    elif chall == 2:
        print(part2())
    else:
        print("You need to enter either 1 or 2")
        exit(1)


def test():
    s = "dim silver bags contain 2 shiny chartreuse bags, 4 dull magenta bags."
    t = "plaid beige bags contain 3 drab magenta bags."
    r = "mirrored gold bags contain no other bags."
    # print(s.split(sep=' contain ')[0].split(sep=' bags')[0])
    temp = s.split(sep=' contain ')[1].split(', ')
    # print(t.split(sep=' contain ')[1].split(', '))
    # print(r.split(sep=' contain ')[1].split(', '))
    print(' '.join(temp[0].split(sep=' ')[1:3]))

# test()
run()
