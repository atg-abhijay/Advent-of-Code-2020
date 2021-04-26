"""
URL for challenge: https://adventofcode.com/2020/day/25
"""


def process_input():
    f = open("advent-25-input.txt")
    card_pubkey = int(f.readline().rstrip())
    door_pubkey = int(f.readline().rstrip())

    return card_pubkey, door_pubkey


def part1():
    card_pubkey, door_pubkey = process_input()
    initial_subject_number, divisor = 7, 20201227
    value, card_loop_size = 1, 0
    while value != card_pubkey:
        value *= initial_subject_number
        value %= divisor
        card_loop_size += 1

    encryption_key = 1
    for _ in range(card_loop_size):
        encryption_key *= door_pubkey
        encryption_key %= divisor

    return encryption_key


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
