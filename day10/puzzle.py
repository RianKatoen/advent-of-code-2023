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
        
    elif pipes[i2][j2] == 'L' and i1 < i2:
        return [(i2, j2 - 1), (i2 + 1, j2)]
    elif pipes[i2][j2] == 'J' and j1 < j2:
        return [(i2 + 1, j2), (i2, j2 + 1)]
    elif pipes[i2][j2] == '7' and i2 < i1:
        return [(i2 - 1, j2), (i2, j2 + 1)]
    elif pipes[i2][j2] == 'F' and j2 < j1: 
        return [(i2 - 1, j2), (i2, j2 - 1)]
    else:
        return []

def turn_left(start: tuple[int, int], dest: tuple[int, int], pipes: list[str]) -> list[tuple[int, int]]:
    i1, j1 = start
    i2, j2 = dest
    
    i = i2 - i1
    j = j2 - j1

    if pipes[i2][j2] == '-' or pipes[i2][j2] == '|':
        if i == 0 and j == 1:
            return [(i2 - 1, j2)]
        elif i == 1 and j == 0:
            return [(i2, j2 + 1)]
        elif i == 0 and j == -1:
            return [(i2 + 1, j2)]
        elif i == -1 and j == 0:
            return [(i2, j2 - 1)]
    else:
        return []

def part2(file: str, verbosity: int = 0) -> int:
    print("")
    print(traverse(file, lambda s, d, p: turn_right(s, d, p), verbosity))
    #print(traverse(file, lambda s, d, p: turn_left(s, d, p), verbosity))
    return 0

def get_externals(pipes: tuple[list[str]]) -> set[tuple[int, int]]:
    n_rows, n_cols = len(pipes), len(pipes[0])

    externals = set()
    for i in range(0, n_rows):
        for j in range(0, n_cols):
            if pipes[i][j] != '.':
                break
            externals.add((i, j))

    for i in range(0, n_rows):
        for j in range(0, n_cols)[::-1]:
            if pipes[i][j] != '.':
                break
            externals.add((i, j))

    for j in range(0, n_cols):
        for i in range(0, n_rows):
            if pipes[i][j] != '.':
                break
            externals.add((i, j))

    for j in range(0, n_cols)[::-1]:
        for i in range(0, n_rows):
            if pipes[i][j] != '.':
                break
            externals.add((i, j))

    return externals

def traverse(file: str, turner_fn, verbosity: int = 0) -> int:
    pipes = input(file)
    externals = get_externals(pipes)
    start = find_starting_position(pipes)
    destinations = find_start(start, pipes)

    n_rows, n_cols = len(pipes), len(pipes[0])
    if verbosity > 0:
        print(file, " [starting position] ", start)
        print(file, " [destinations] ", destinations)
    
    all_tiles = []
    for destination in destinations:
        path = set()
        path.add(start)
        tiles = set()
    
        i1, j1 = start
        i2, j2 = destination
        if verbosity > 1:
            print("")
            print(file, " [right_track] ", pipes[start[0]][start[1]], start, "->", pipes[destination[0]][destination[1]], destination)

        while destination != start:
            path.add(destination)
            i2, j2 = destination
            turns = turner_fn((i1, j1), (i2, j2), pipes)
            for i3, j3 in turns:
                if (i3, j3) in externals or i3 < 0 or j3 < 0:
                    tiles = set()
                elif i3 >= 0 and j3 >= 0 and i3 < n_rows and j3 < n_cols:
                    if verbosity > 1:
                        print(file, " [turn] ", (i3, j3))
                    tiles.add((i3, j3))

            destination = move((i1, j1), (i2, j2), pipes)

            i1, j1 = i2, j2
            if verbosity > 1:
                print(file, " [next_destination] ", pipes[i1][j1], (i1, j1), "->", pipes[destination[0]][destination[1]], destination)

        for tile in [t for t in tiles]:
            if tile in path:
                tiles.remove(tile)

        if verbosity > 1:
            for tile in [t for t in tiles]:
                print(file, " [tile] ", tile)

        all_tiles.append(tiles)

    return max([len(tiles) for tiles in all_tiles])
    
print("example 1:", part2(f"example1.txt", 0))
print("example 3:", part2(f"example3.txt", 0))
print("example 4:", part2(f"example4.txt", 0))
print("example 5:", part2(f"example5.txt", 0))
print("example 6:", part2(f"example6.txt", 0))
print("example 7:", part2(f"example7.txt", 0))
print("part 2:", part2(f"input.txt", 0))