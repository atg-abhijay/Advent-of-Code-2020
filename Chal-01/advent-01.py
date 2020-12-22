"""
URL for challenge: https://adventofcode.com/2020/day/1
"""

def main():
    return

def part1(parsed_data):
    return

def part2(parsed_data):
    return

def run():
    chall = int(input("Please enter either 1 or 2 for the challenges: "))
    parsed_data = main()
    if chall == 1:
        part1(parsed_data)
    elif chall == 2:
        part2(parsed_data)
    else:
        print("You need to enter either 1 or 2")
        exit(1)

run()
