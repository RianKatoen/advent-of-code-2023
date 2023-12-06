import re

def input(file: str) -> tuple[list[int], list[list[tuple[tuple[int, int, int], tuple[int, int, int]]]]]:
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
                y1, x1, length = tuple(int(search.group(i)) for i in range(1, 4))
                intermediate.append(((x1, x1 + length - 1), (y1, y1 + length - 1)))
            
            if line.strip() == "" and len(intermediate) > 0:
                intermediate.sort(key=lambda range: range[0])
                maps.append(intermediate)
                intermediate=[]

    intermediate.sort(key=lambda range: range[0])
    maps.append(intermediate)
    intermediate=[]

    return (seeds, maps)

def find_new_loc(pos: int, ranges: list[tuple[tuple[int, int], tuple[int, int]]]) -> int:
    for ((x1, x2), (y1, _)) in ranges:
        if pos >= x1 and pos <= x2:
            return y1 + (pos - x1)
    
    return pos

from enum import Enum

EMPTY = ((-99, -99), (-99, -99))

# class syntax
class Preceeding(Enum):
    NONE = 1
    PARTIAL = 2
    COMPLETE = 3

def assert_equal(result, expected):
    if result == expected:
        print(result)
    else:
        raise Exception(result, " is unequal to ", expected)

def is_preceeding(range1: tuple[tuple[int, int], tuple[int, int]], range2: tuple[tuple[int, int], tuple[int, int]]) -> tuple[Preceeding, tuple[tuple[int, int], tuple[int, int]]]:
    (x1, x2), (xy1, xy2) = range1
    (y1, y2), (z1, z2) = range2

    # preceeding
    if xy1 < y1:
        if xy2 < y1:
            return Preceeding.COMPLETE, ((x1, x2), (xy1, xy2))
        else:
            xy2 = y1 - 1
            x2 = x1 + (xy2 - xy1)
            return Preceeding.PARTIAL, ((x1, x2), (xy1, xy2))
    else:
        return Preceeding.NONE, EMPTY

print("")
print("Tests preceeding")
assert_equal(is_preceeding(((10, 15), (5, 10)), ((15, 20), (5, 10))), (Preceeding.COMPLETE, ((10, 15), (5, 10))))
assert_equal(is_preceeding(((10, 15), (5, 10)), ((7, 10), (5, 10))), (Preceeding.PARTIAL, ((10, 11), (5, 6))))
assert_equal(is_preceeding(((10, 15), (7, 10)), ((7, 10), (5, 10))), (Preceeding.NONE, EMPTY))
assert_equal(is_preceeding(((98, 99), (50, 51)), ((15, 51), (0, 36))), (Preceeding.NONE, EMPTY))
assert_equal(is_preceeding(((0, 36), (15, 51)), ((50, 51), (98, 99))), (Preceeding.PARTIAL, ((0, 34), (15, 49))))
assert_equal(is_preceeding(((98, 99), (50, 51)), ((50, 51), (35, 36))), (Preceeding.NONE, EMPTY))
assert_equal(is_preceeding(((82, 92), (46, 56)), ((56, 92), (60, 96))), (Preceeding.PARTIAL, ((82, 91), (46, 55))))

# class syntax
class Overlapping(Enum):
    NO = 1
    YES = 2

def is_overlapping(range1: tuple[tuple[int, int], tuple[int, int]], range2: tuple[tuple[int, int], tuple[int, int]]) -> tuple[Overlapping, tuple[tuple[int, int], tuple[int, int]]]:
    (x1, x2), (xy1, xy2) = range1
    (y1, y2), (z1, z2) = range2

    if (xy2 >= y1 and xy1 <= y2) or (y2 >= xy1 and y1 <= xy2):
        new_y1 = max(xy1, y1)
        new_y2 = min(xy2, y2)

        x1 += new_y1 - xy1
        x2 += new_y2 - xy2

        z1 += new_y1 - y1
        z2 += new_y2 - y2

        return Overlapping.YES, ((x1, x2), (z1, z2))
    else:
        return Overlapping.NO, EMPTY

print("")
print("Tests overlapping")
assert_equal(is_overlapping(((10, 15), (10, 15)), ((20, 25), (5, 10))), (Overlapping.NO, EMPTY))
assert_equal(is_overlapping(((20, 25), (30, 35)), ((30, 35), (5, 10))), (Overlapping.YES, ((20, 25), (5, 10))))
assert_equal(is_overlapping(((20, 25), (30, 35)), ((32, 33), (7, 8))), (Overlapping.YES, ((22, 23), (7, 8))))
assert_equal(is_overlapping(((20, 25), (30, 35)), ((32, 40), (7, 15))), (Overlapping.YES, ((22, 25), (7, 10))))
assert_equal(is_overlapping(((20, 25), (30, 35)), ((28, 30), (7, 9))), (Overlapping.YES, ((20, 20), (9, 9))))
assert_equal(is_overlapping(((98, 99), (50, 51)), ((50, 51), (35, 36))), (Overlapping.YES, ((98, 99), (35, 36))))

def overlap_range(sources_list: list[tuple[tuple[int, int], tuple[int, int]]], targets_list: list[tuple[tuple[int, int], tuple[int, int]]]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    # ensure sorting is in line with each other
    sources_list.sort(key = lambda s: s[1][0])
    targets_list.sort(key = lambda s: s[0][0])

    sources = iter(sources_list)
    targets = iter(targets_list)
    
    new_targets = []
    counter = 0
    (x1, x2), (xy1, xy2) = (-1, -1), (-1, -1)
    (y1, y2), (z1, z2) = (-1, -1), (-1, -1)
    while counter <= 500 and (x1 != -99 or y1 != -99):
        counter += 1

        if x1 == -1 or x2 < x1:
            (x1, x2), (xy1, xy2) = next(sources, ((-99, -99), (-99, -99)))

        if y1 == -1 or y2 < y1:
            (y1, y2), (z1, z2) = next(targets, ((-99, -99), (-99, -99)))

        if x1 != -99 and y1 == -99:
            new_targets.append(((x1, x2), (xy1, xy2)))
            x1 = -1
            continue
        
        if y1 != -99 and x1 == -99:
            y1 = -1
            continue

        if y1 == -99 and x1 == -99:
            continue

        if x1 < 0 or y1 < 0:
            raise Exception("WUT")

        preceeding, preceeding_source = is_preceeding(((x1, x2), (xy1, xy2)), ((y1, y2), (z1, z2)))
        if preceeding == Preceeding.COMPLETE:
            new_targets.append(preceeding_source)
            x1 = -1
            continue

        if preceeding == Preceeding.PARTIAL:
            new_targets.append(preceeding_source)
            x1 = preceeding_source[0][1] + 1
            xy1 = preceeding_source[1][1] + 1
            continue

        preceeding, preceeding_target = is_preceeding(((z1, z2), (y1, y2)), ((xy1, xy2), (x1, x2)))
        if preceeding == Preceeding.COMPLETE:
            y1 = -1
            continue

        if preceeding == Preceeding.PARTIAL:
            y1 = preceeding_target[1][1] + 1
            z1 = preceeding_target[0][1] + 1
            continue

        overlapping, overlapping_range = is_overlapping(((x1, x2), (xy1, xy2)), ((y1, y2), (z1, z2)))
        if overlapping == Overlapping.YES:
            new_targets.append(overlapping_range)
            length = overlapping_range[0][1] - overlapping_range[0][0] + 1
            x1 += length
            xy1 += length
            y1 += length
            z1 += length

            continue
        
        raise Exception("WUT")

    return new_targets

def part1(file: str) -> int:
    seeds, maps = input(file)
    seeds = [((s, s), (s, s))  for s in seeds]
    for map in maps:
        seeds = overlap_range(seeds, map)

    return min([s[1][0] for s in seeds])

def part2(file: str):
    seeds, maps = input(file)
    seeds = [((seeds[i], seeds[i] + seeds[i+1] - 1), (seeds[i], seeds[i] + seeds[i+1] - 1))  for i in range(0, len(seeds), 2)]
    for map in maps:
        seeds = overlap_range(seeds, map)

    return min([s[1][0] for s in seeds])

print("")
print("example 1:", part1("example1.txt"))
print("part 1:", part1("input.txt"))

print("")
print("example 2:", part2("example1.txt"))
print("part 2:", part2("input.txt"))