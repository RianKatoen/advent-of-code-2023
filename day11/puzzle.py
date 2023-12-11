from itertools import combinations

def input(file: str) -> list[list[str]]:
    with open(file, "r") as input:
        return([line.strip() for line in input])

def inflate_map(map: list[list[str]]) -> list[list[str]]:
    n_rows, n_cols = len(map), len(map[0])
    new_map = []
    for row in map:
        new_map.append(row)
        if all(r == '.' for r in row):
            new_map.append('0' * len(row))
    
    i = 0
    while i < len(new_map[0]):
        if all(r[i] == '.' or r[i] == '0' for r in new_map):
            for r, j in zip(new_map, range(len(new_map))):
                new_map[j] = r[0:i] + '0' + r[i:]
            i += 1
        i += 1

    return new_map

def find_galaxies(map: list[list[str]], inflation_factor: int = 2) -> set[tuple[int, int]]:
    galaxies: set[tuple[int, int]] = set()

    row = 0
    for i in range(len(map)):
        col = 0
        for j in range(len(map[0])):
            if map[i][j] == '#':
                galaxies.add((row, col))
            
            col += (inflation_factor - 1) if map[i][j] == '0' else 1
        
        row += (inflation_factor - 1) if map[i][0] == '0' else 1

    return galaxies
    
def find_pairs(galaxies: set[tuple[int, int]]) -> set[tuple[int, int], tuple[int, int]]:
    pairs: set[tuple[int, int], tuple[int, int]] = set()
    return set(combinations(galaxies, 2))
    
def calculate_distance(galaxy1: tuple[int, int], galaxy2: tuple[int, int]) -> int:
    i1, j1 = galaxy1
    i2, j2 = galaxy2
    return abs(i1 - i2) + abs(j1 - j2)

def sum_of_distances(file: str, inflation_factor: int = 2) -> int:
    map = input(file)
    map = inflate_map(map)
    galaxies = find_galaxies(map, inflation_factor)
    pairs = find_pairs(galaxies)

    return sum(calculate_distance(g1, g2) for g1, g2 in pairs)

print("example 1:", sum_of_distances("example1.txt"))
print("part 1:", sum_of_distances("input.txt"))

print("")
print("example 2:", sum_of_distances("example1.txt", 10))
print("example 2:", sum_of_distances("example1.txt", 100))
print("part 2:", sum_of_distances("input.txt", 1000000))