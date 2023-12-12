import re
from itertools import permutations

def input(file: str) -> list[tuple[str, str]]:
    with open(file, "r") as input:
        return([tuple(line.strip().split(' ')) for line in input])

def get_options(line: str) -> list[str]:
    if len(line) == 1:
        match line:
            case '?': return ['.', '#']
            case _: return [line]
    else:
        options = []
        for o in get_options(line[1:]):
            for v in get_options(line[0]):
                options.append(v + o)
        return options
    

def get_springs(line: str) -> list[int]:
    return([int(i) for i in line.split(',')])


def part1(file: str) -> int:
    info = [(get_options(o), get_springs(s)) for o, s in input(file)]
    pattern = re.compile(r'(?<!#)(#+)(?!#)')
    n_legit_setups = 0
    for options, springs in info:
        total_springs = sum(springs)
        for o in [o for o in options if o.count('#') == total_springs]:
            locs = pattern.findall(o)
            if len(locs) == len(springs) and all(len(l) == s for l, s in zip(locs, springs)):
                n_legit_setups += 1

    return n_legit_setups

print("example 1:", part1("example1.txt"))
print("part 1:", part1("input.txt"))