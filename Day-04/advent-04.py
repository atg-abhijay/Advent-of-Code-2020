"""
URL for challenge: https://adventofcode.com/2020/day/4
"""

def part1():
    f = open("advent-04-input.txt")
    passports = [{}]
    for line in f.readlines():
        if line == '\n':
            passports.append({})
            continue

        line_data = line.strip().split(sep=' ')
        for kv in line_data:
            key, value = kv.split(sep=':')
            passports[-1][key] = value

    required_fields = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"])

    num_valid_papos = 0
    for papo in passports:
        papo_fields = set(papo.keys())
        num_fields = len(papo_fields)
        if num_fields > 8 or num_fields < 7:
            continue

        if num_fields == 7 and "cid" in papo_fields:
            continue

        if num_fields == 8 and not papo_fields.__eq__(required_fields):
            continue

        num_valid_papos += 1

    return num_valid_papos

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
