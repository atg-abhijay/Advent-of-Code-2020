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

        checks = [
            check_birth_year, check_issue_year, check_expiration_year,
            check_height, check_hair_color, check_eye_color, check_passport_id
        ]

        if all((check(papo) for check in checks)):
            num_valid_papos += 1

    return num_valid_papos


def check_birth_year(passport):
    birth_yr = int(passport["byr"])
    if birth_yr < 1920 or birth_yr > 2002:
        return False

    return True


def check_issue_year(passport):
    issue_yr = int(passport["iyr"])
    if issue_yr < 2010 or issue_yr > 2020:
        return False

    return True


def check_expiration_year(passport):
    expiration_yr = int(passport["eyr"])
    if expiration_yr < 2020 or expiration_yr > 2030:
        return False

    return True


def check_height(passport):
    height = passport["hgt"]
    height_value = int(height[:-2])
    if height[-2:] not in ["cm", "in"]:
        return False

    if height[-2:] == "cm" and (height_value < 150 or height_value > 193):
        return False

    if height[-2:] == "in" and (height_value < 59 or height_value > 76):
        return False

    return True


def check_hair_color(passport):
    hair_color = passport["hcl"]
    if len(hair_color) != 7 or hair_color[0] != "#":
        return False

    allowed_chars = set(string.digits + 'abcdef')
    if not set(hair_color[1:]).issubset(allowed_chars):
        return False

    return True


def check_eye_color(passport):
    eye_color = passport["ecl"]
    valid_eye_colors = set(
        ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    if eye_color not in valid_eye_colors:
        return False

    return True


def check_passport_id(passport):
    passport_id = passport["pid"]
    if len(passport_id) != 9 or not set(passport_id).issubset(string.digits):
        return False

    return True


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
