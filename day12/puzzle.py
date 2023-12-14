import re
from itertools import permutations
from typing import Generator

def input(file: str) -> list[tuple[str, str]]:
    with open(file, "r") as input:
        return([tuple(line.strip().split(' ')) for line in input])

def get_options(line: str, max_hash: int, hash_count: int, q_count: int) -> Generator[tuple[int, int, str], None, None]:
    if len(line) == 0:
        yield (hash_count, q_count, line)
    elif hash_count == max_hash:
        yield (hash_count, q_count, line)
    elif hash_count < max_hash and q_count + hash_count >= max_hash:
        q_ix = line.find('?')
        for hc2, qc2, o in get_options(line[(q_ix + 1):], max_hash, hash_count, q_count - 1):
            yield (hc2, qc2, line[0:q_ix] + '.' + o)
        
        for hc2, qc2, o in get_options(line[(q_ix + 1):], max_hash, hash_count + 1, q_count - 1):
            yield (hc2, qc2, line[0:q_ix] + '#' + o)

def get_springs(line: str) -> list[int]:
    return([int(i) for i in line.split(',')])

def part1(file: str) -> int:
    info = ((get_options(o, sum(get_springs(s)), o.count('#'), o.count('?')), get_springs(s)) for o, s in input(file))
    pattern = re.compile(r'(?<!#)(#+)(?!#)')
    n_legit_setups = 0
    i = 0
    for options, springs in info:
        for _, _, o in options:
            locs = pattern.findall(o)
            if len(locs) == len(springs) and all(len(l) == s for l, s in zip(locs, springs)):
                n_legit_setups += 1

    return n_legit_setups

print("example 1", part1("example1.txt"))
print("part 1:", part1("input.txt"))

def part2(file: str) -> int:
    for o, s in input(file):
        print(o, s)
    return 0

#print("example 2:", part2("example1.txt"))