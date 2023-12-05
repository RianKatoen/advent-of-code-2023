import re

def input(file: str) -> tuple[list[int], list[list[tuple[int, int, int]]]]:
    seeds = []
    maps = []
    intermediate = []
    pattern = re.compile(r'(\d+)\s(\d+)\s(\d+)')
    with open(file, "r") as input:
        for line in input:
            if len(seeds) == 0:
                seeds = [int(i) for i in re.sub(r'seeds: ', '', line).strip().split(' ')]
                continue

            search = pattern.search(line)
            if search:
                intermediate.append(tuple(int(search.group(i)) for i in range(1, 4)))
            
            if line.strip() == "" and len(intermediate) > 0:
                intermediate.sort(key=lambda range: range[0])
                maps.append(intermediate)
                intermediate=[]

    intermediate.sort(key=lambda range: range[0])
    maps.append(intermediate)
    intermediate=[]

    return (seeds, maps)

def find_new_loc(pos: int, ranges: list[tuple[int, int, int]]) -> int:
    for (new_start,start, length) in ranges:
        if pos >= start and pos <= start + length:
            return new_start + (pos - start)
    
    return pos

def part1(file: str) -> int:
    seeds, maps = input(file)
    locs = []
    for loc in seeds:
        for map in maps:
            loc = find_new_loc(loc, map)
        locs.append(loc)

    return min(locs)

print("example 1:", part1("example1.txt"))
print("part 1:", part1("input.txt"))