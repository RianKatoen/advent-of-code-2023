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
            
def part3(file: str, verbosity: int = 0) -> int:
    pipes = input(file)
    start = find_starting_position(pipes)
    destinations = find_start(start, pipes)
    n_rows, n_cols = len(pipes), len(pipes[0])

    path = set()
    path.add(start)
    (i1, j1), destination = start, destinations[0]

    while destination != start:
        path.add(destination)
        (i2, j2) = destination
        destination = move((i1, j1), (i2, j2), pipes)
        (i1, j1) = (i2, j2)

    new_maps = []
    for i in range(n_rows):
        row = ""
        for j in range(n_cols):
            if (i, j) in path:
                row = row + pipes[i][j]
            else:
                row = row + " "
        
        new_maps.append(row)
        if verbosity == -1:
            print(row)
    
    return 0

print("example 1:", part3(f"example1.txt", -1))
print("example 3:", part3(f"example3.txt", -1))
print("example 4:", part3(f"example4.txt", -1))
print("example 5:", part3(f"example5.txt", -1))
print("example 6:", part3(f"example6.txt", -1))
print("example 7:", part3(f"example7.txt", -1))
print("part 2:", part3(f"input.txt", -1))
print("custom 1:", part3(f"custom1.txt", -1))
