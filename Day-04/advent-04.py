"""
URL for challenge: https://adventofcode.com/2020/day/4
"""

import string


def process_input():
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

    return passports


def part1_verification(papo):
    valid_fields = set(["byr", "iyr", "eyr", "hgt",
                        "hcl", "ecl", "pid", "cid"])
    papo_fields = set(papo.keys())
    num_fields = len(papo_fields)
    if num_fields > 8 or num_fields < 7:
        return False

    if num_fields == 7 and "cid" in papo_fields:
        return False

    if num_fields == 8 and not papo_fields.__eq__(valid_fields):
        return False

    return True


def part1():
    passports = process_input()
    num_valid_papos = 0

    for papo in passports:
        if part1_verification(papo):
            num_valid_papos += 1

    return num_valid_papos


def part2():
    passports = process_input()
    num_valid_papos = 0

    for papo in passports:
        if not part1_verification(papo):
            continue

        # Birth year
        birth_yr = int(papo["byr"])
        if birth_yr < 1920 or birth_yr > 2002:
            continue

        # Issue year
        issue_yr = int(papo["iyr"])
        if issue_yr < 2010 or issue_yr > 2020:
            continue

        # Expiration year
        expiration_yr = int(papo["eyr"])
        if expiration_yr < 2020 or expiration_yr > 2030:
            continue

        # Height
        height = papo["hgt"]
        height_value = int(height[:-2])
        if height[-2:] not in ["cm", "in"]:
            continue

        if height[-2:] == "cm" and (height_value < 150 or height_value > 193):
            continue

        elif height[-2:] == "in" and (height_value < 59 or height_value > 76):
            continue

        # Hair color
        hair_color = papo["hcl"]
        if len(hair_color) != 7 or hair_color[0] != "#":
            continue

        allowed_chars = set(string.digits + 'abcdef')
        if not set(hair_color[1:]).issubset(allowed_chars):
            continue

        # Eye color
        eye_color = papo["ecl"]
        valid_eye_colors = set(
            ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
        if eye_color not in valid_eye_colors:
            continue

        # Passport ID
        passport_id = papo["pid"]
        if len(passport_id) != 9 or not set(passport_id).issubset(string.digits):
            continue

        num_valid_papos += 1

    return num_valid_papos


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
