"""
URL for challenge: https://adventofcode.com/2020/day/22
"""


from collections import deque
from itertools import islice


def process_input():
    f = open("advent-22-input.txt")
    p1_cards, p2_cards = deque(), deque()
    idx, puzzle_input = 0, f.readlines()[1:]
    for line in puzzle_input:
        if line != '\n':
            p1_cards.append(int(line.strip()))
            idx += 1
        else:
            break

    for line in puzzle_input[idx+2:]:
        p2_cards.append(int(line.strip()))

    return p1_cards, p2_cards


def part1():
    p1_cards, p2_cards = process_input()
    while p1_cards and p2_cards:
        p1_top, p2_top = p1_cards.popleft(), p2_cards.popleft()
        if p1_top > p2_top:
            p1_cards.extend([p1_top, p2_top])
        else:
            p2_cards.extend([p2_top, p1_top])

    return calculate_score(p1_cards if p1_cards else p2_cards)


def part2():
    p1_cards, p2_cards = process_input()
    winner_deck = p1_cards if play_game(p1_cards, p2_cards) == 1 else p2_cards
    return calculate_score(winner_deck)


def calculate_score(winner_deck):
    score, num_cards = 0, len(winner_deck)
    for card in winner_deck:
        score += card * num_cards
        num_cards -= 1

    return score


def play_game(p1_cards, p2_cards):
    previous_configs = set()
    p1_num_cards, p2_num_cards = len(p1_cards), len(p2_cards)
    while p1_cards and p2_cards:
        current_config = (tuple(p1_cards), tuple(p2_cards))
        if current_config in previous_configs:
            return 1

        previous_configs.add(current_config)
        p1_top, p2_top = p1_cards.popleft(), p2_cards.popleft()
        p1_num_cards -= 1
        p2_num_cards -= 1

        if p1_num_cards >= p1_top and p2_num_cards >= p2_top:
            subgame_p1_cards = deque(islice(p1_cards, p1_top))
            subgame_p2_cards = deque(islice(p2_cards, p2_top))
            winner = play_game(subgame_p1_cards, subgame_p2_cards)
        else:
            winner = 1 if p1_top > p2_top else 2

        if winner == 1:
            p1_cards.extend([p1_top, p2_top])
            p1_num_cards += 2
        else:
            p2_cards.extend([p2_top, p1_top])
            p2_num_cards += 2

    return winner


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
