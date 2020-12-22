"""
URL for challenge: https://adventofcode.com/2020/day/2
"""

def main():
    return

def part1(parsed_data):
    f = open("advent-02-input.txt")
    num_valid_pwds = 0
    for policy_pwd in f.readlines():
        limits, letter, pwd = policy_pwd.split(sep=' ')
        lower_lim, upper_lim = [int(li) for li in limits.split(sep='-')]
        letter = letter[0]

        letter_count = 0
        for char in pwd:
            if char == letter:
                letter_count += 1

        if letter_count >= lower_lim and letter_count <= upper_lim:
            num_valid_pwds += 1

    return num_valid_pwds

def part2(parsed_data):
    f = open("advent-02-input.txt")
    num_valid_pwds = 0
    for policy_pwd in f.readlines():
        indices, letter, pwd = policy_pwd.split(sep=' ')
        lower_idx, upper_idx = [int(idx) for idx in indices.split(sep='-')]
        letter = letter[0]

        first_case = pwd[lower_idx-1] == letter
        second_case = pwd[upper_idx-1] == letter

        if first_case ^ second_case:
            num_valid_pwds += 1

    return num_valid_pwds

def run():
    chall = int(input("Please enter either 1 or 2 for the challenges: "))
    parsed_data = main()
    if chall == 1:
        print(part1(parsed_data))
    elif chall == 2:
        print(part2(parsed_data))
    else:
        print("You need to enter either 1 or 2")
        exit(1)

run()
