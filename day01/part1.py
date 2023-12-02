import re

def input(file):
    lines = []
    with open(file, "r") as input:
        for line in input:
            lines.append(line.strip())
    return lines

def calibration_values(file, digit_pattern):
    re_two_digits_pattern = re.compile(digit_pattern + '.*' + digit_pattern)
    re_one_digit_pattern = re.compile(digit_pattern)

    results = []
    for line in input(file):
        search  = re_two_digits_pattern.search(line)
        if search:
            results.append([search.group(1), search.group(2)])
            continue
        search = re_one_digit_pattern.search(line)
        if search:
            results.append([search.group(1), search.group(1)])

    return results

def part1(file):
    results = calibration_values(file, r'([0-9]{1})')
    total = 0
    for result in results:
        total += int(result[0] + result[1])
    return total

print("example 1:", part1("example1.txt"))
print("part 1:", part1("input.txt"))

def string_to_number(val):
    numbers = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }

    if len(val) > 1:
        return numbers[val]
    else:
        return val

def part2(file):
    results = calibration_values(file, r'(\d|one|two|three|four|five|six|seven|eight|nine){1}')

    total = 0
    for result in results:
        total += int(string_to_number(result[0]) + string_to_number(result[1]))
    return total

print("example 2:", part2("example2.txt"))
print("part 2:", part2("input.txt"))