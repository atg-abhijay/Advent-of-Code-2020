"""
URL for challenge: https://adventofcode.com/2020/day/25
"""


def process_input():
    f = open("advent-25-input.txt")
    card_pubkey = int(f.readline().rstrip())
    door_pubkey = int(f.readline().rstrip())

    return card_pubkey, door_pubkey


def part1():
    return


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


run()
