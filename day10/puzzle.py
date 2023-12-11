import re

def input(file: str) -> tuple[list[str]]:
    with open(file, "r") as input:
            return([line.strip() for line in input])

def find_starting_position(pipes: list[str]) -> tuple[int, int]:
    i = 0
    for pipe in pipes:
        j = 0
        for p in pipe:
            # S is the starting position of the animal; there is a pipe on this
            if p == 'S':
                return (i, j)
            j += 1
        i += 1

    return (-1, -1)

def find_start(start: tuple[int, int], pipes: list[str]) -> tuple[tuple[int, int], list[tuple[int, int]]]:
    i1, j1 = start
    destinations = []
    for i2 in range(i1 - 1, i1 + 2):
        for j2 in range(j1 - 1, j1 + 2):
            if i1 == i2 and j1 == j2:
                continue
            elif abs(i1 - i2) + abs(j1 - j2) > 1:
                continue
            elif i2 < 0 or j2 < 0:
                continue
            elif i2 >= len(pipes) or j2 >= len(pipes[i2]):
                continue
            elif pipes[i2][j2] == '.':
                continue

            match pipes[i2][j2]:
                # | is a vertical pipe connecting north and south.
                case '|':
                    if i2 != i1 and j2 == j1:
                        destinations.append((i2, j2))
                # - is a horizontal pipe connecting east and west.        
                case '-':
                    if i2 == i1 and j2 != j1:
                        destinations.append((i2, j2))
                # L is a 90-degree bend connecting north and east.
                case 'L':
                    if (i2 > i1 and j2 == j1) or (i2 == i1 and j2 < j1):
                        destinations.append((i2, j2))
                # J is a 90-degree bend connecting north and west.
                case 'J':
                    if (i2 > i1 and j2 == j1) or (i2 == i1 and j2 > j1):
                        destinations.append((i2, j2))
                # 7 is a 90-degree bend connecting south and west.
                case '7':
                    if (i2 < i1 and j2 == j1) or (i2 == i1 and j2 > j1):
                        destinations.append((i2, j2))
                # F is a 90-degree bend connecting south and east.
                case 'F':
                    if (i2 < i1 and j2 == j1) or (i2 == i1 and j2 < j1):
                        destinations.append((i2, j2))
            
    return destinations

                

def move(start: tuple[int, int], dest: tuple[int, int], pipes: list[str], raise_exception: bool = True) -> tuple[int, int]:
    i1, j1 = start
    i2, j2 = dest
    
    match pipes[i2][j2]:
        # | is a vertical pipe connecting north and south.
        case '|':
            return (i2 + 1, j2) if i2 > i1 else (i2 - 1, j2)
        # - is a horizontal pipe connecting east and west.        
        case '-':
            return (i2, j2 + 1) if j2 > j1 else (i2, j2 - 1)
        # L is a 90-degree bend connecting north and east.
        case 'L':
            return (i2, j2 + 1) if i2 > i1 else (i2 - 1, j2)
        # J is a 90-degree bend connecting north and west.
        case 'J':
            return (i2 - 1, j2) if j2 > j1 else (i2, j2 - 1)
        # 7 is a 90-degree bend connecting south and west.
        case '7':
            return (i2 + 1, j2) if j2 > j1 else (i2, j2 - 1)
        # F is a 90-degree bend connecting south and east.
        case 'F':
            return (i2, j2 + 1) if i2 < i1 else (i2 + 1, j2)
        # . is ground; there is no pipe in this tile.
        # S is the starting position of the animal; there is a pipe on this
        case _:
            if raise_exception:
                raise Exception("Can't enter "  + pipes[i2][j2] + " at " + f"({start[0]}, {start[1]})" + " to " + f"({dest[0]}, {dest[1]})")
            else:
                return (-1, -1)

def part1(file: str, verbosity: int = 0) -> int:
    pipes = input(file)
    start = find_starting_position(pipes)
    destinations = find_start(start, pipes)

    if verbosity > 0:
        print(file, " [starting position] ", start)
        print(file, " [destinations] ", destinations)

    max_moves: dict[tuple[int, int], int] = { start: 0 }
    for destination in destinations:
        n_moves = 1
        i1, j1 = start
        if verbosity > 1:
            print(file, " [next_destination] ", pipes[start[0]][start[1]], start, "->", pipes[destination[0]][destination[1]], destination, f' [{n_moves}]')
        while destination != start:
            if not destination in max_moves.keys():
                max_moves[destination] = n_moves
            elif n_moves < max_moves[destination]:
                max_moves[destination] = n_moves
            else:
                break

            i2, j2 = destination
            destination = move((i1, j1), (i2, j2), pipes)
            i1, j1 = i2, j2
            if verbosity > 1:
                print(file, " [next_destination] ", pipes[i1][j1], (i1, j1), "->", pipes[destination[0]][destination[1]], destination , f' [{n_moves}]')
            n_moves += 1       
        
        if verbosity > 1:
            print("")

    return max([n_moves for n_moves in max_moves.values()])

for i in range(1, 3):
    print(f"example {i}:", part1(f"example{i}.txt", 0))
print("part 1:", part1(f"input.txt", 0))
print("")

def turn_right(start: tuple[int, int], dest: tuple[int, int], pipes: list[str]) -> list[tuple[int, int]]:
    i1, j1 = start
    i2, j2 = dest
    
    if pipes[i2][j2] == '-':
        if j2 > j1:
            return [(i2 + 1, j2)]
        else:
            return [(i2 - 1, j2)]
        
    elif pipes[i2][j2] == '|':
        if i2 > i1:
            return [(i2, j2 - 1)]
        else:
            return [(i2, j2 + 1)]

    # L is a 90-degree bend connecting north and east.
    elif pipes[i2][j2] == 'L' and i2 > i1:
        return [(i2, j2 - 1), (i2 + 1, j2), (i2 + 1, j2 + 1)]
    # J is a 90-degree bend connecting north and west.
    elif pipes[i2][j2] == 'J' and j2 > j1:
        return [(i2 + 1, j2), (i2, j2 + 1), (i2 + 1, j2 + 1)]
    # 7 is a 90-degree bend connecting south and west.
    elif pipes[i2][j2] == '7' and i2 < i1:
        return [(i2 - 1, j2), (i2, j2 + 1), (i2 - 1, j2 + 1)]
    # F is a 90-degree bend connecting south and east.
    elif pipes[i2][j2] == 'F' and j2 < j1: 
        return [(i2 - 1, j2), (i2, j2 - 1), (i2 - 1, j2 - 1)]
    else:
        return []

def part2(file: str, verbosity: int = 0) -> int:
    return traverse(file, verbosity)

def traverse(file: str, verbosity: int = 0) -> int:
    pipes = input(file)
    start = find_starting_position(pipes)
    destinations = find_start(start, pipes)

    n_rows, n_cols = len(pipes), len(pipes[0])
    for i in range(n_rows):
        for j in range(n_cols):
            if pipes[i][j] != 'S':
                pipes[i].replace('S', '-')

    if verbosity > 0:
        print(file, " [starting position] ", start)
        print(file, " [destinations] ", destinations)
    
    all_n_tiles = []
    all_tiles = []
    for destination in destinations:
        path = []
        path.append(start)

        i1, j1 = start
        i2, j2 = destination
        if verbosity > 1:
            print("")
            print(file, " [right_track] ", pipes[start[0]][start[1]], start, "->", pipes[destination[0]][destination[1]], destination)

        while destination != start:
            path.append(destination)
            i2, j2 = destination
            destination = move((i1, j1), (i2, j2), pipes)

            i1, j1 = i2, j2
            if verbosity > 1:
                print(file, " [next_destination] ", pipes[i1][j1], (i1, j1), "->", pipes[destination[0]][destination[1]], destination)

        tiles = set()
        any_out_of_bounds = False
        i1, j1 = path[-1]
        for i2, j2 in path:
            turns = turn_right((i1, j1), (i2, j2), pipes)
            i1, j1 = i2, j2
            for i3, j3 in turns:
                if i3 >= 0 and j3 >= 0 and i3 < n_rows and j3 < n_cols:                    
                    if verbosity > 1:
                        print(file, " [turn] ", (i3, j3))
                    tiles.add((i3, j3))
                else:
                    any_out_of_bounds = True
        
        if any_out_of_bounds:
            tiles = set()
            continue

        path = set(path)
        for i, j in [t for t in tiles]:
            if (i, j) in path:
                tiles.remove((i, j))

        if verbosity > 1:
            for tile in [t for t in tiles]:
                print(file, " [tile] ", tile)

        if len(tiles) > 0:
            all_tiles.append(tiles)

        new_maps = []
        for i in range(n_rows):
            row = ""
            for j in range(n_cols):
                if (i, j) in path and pipes[i][j] != 'S':
                    row = row + "0"
                elif (i, j) in tiles:
                    row = row + "+"
                else:
                    row = row + pipes[i][j]
            
            new_maps.append(row)
            if verbosity == -1:
                print(row)

        if verbosity == -1:
            print("")

        n_tiles = len(tiles)
        pattern = re.compile(r'\+([|,F,J,\-,7,L,\.]+)\+')
        for row in new_maps:
            for r in pattern.findall(row):
                n_tiles += len(r)

        all_n_tiles.append(n_tiles)
        
    return [len(tiles) for tiles in all_tiles], all_n_tiles

print("example 1:", part2(f"example1.txt", 0))
print("example 3:", part2(f"example3.txt", 0))
print("example 4:", part2(f"example4.txt", 0))
print("example 5:", part2(f"example5.txt", 0))
print("example 6:", part2(f"example6.txt", 0))
print("example 7:", part2(f"example7.txt", 0))
print("custom 1:", part2(f"custom1.txt", 0))
print("part 2:", part2(f"input.txt", 0))
