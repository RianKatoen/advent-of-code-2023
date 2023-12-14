def input(file: str) -> list[list[str]]:
    with open(file, "r") as input:
        return [[l for l in line.strip()] for line in input]

def transpose(rocks: list[list[str]]) -> list[list[str]]:
    new_rocks = []
    n_lines, n_cols = len(rocks), len(rocks[0])

    for i in range(n_lines):
        new_rock_line = []
        new_rocks.append(new_rock_line)
        for j in range(n_cols):
            new_rock_line.append(rocks[n_cols - j - 1][i])
    
    return new_rocks

def cycle(file: str, n_cycles: int = 0, cycle_size: int = 0) -> int:
    lines = input(file)
    for l, i in zip(lines, range(len(lines))[::-1]):
        l.insert(0, i + 1)
        l.append(i + 1)

    lines.insert(0, [0 for _ in range(len(lines[0]))])
    lines.append([0 for _ in range(len(lines[0]))])

    n_lines, n_cols = len(lines), len(lines[0])
    n_cycles = 1000000000 if n_cycles == 0 else n_cycles
    cycle_size = 4 if cycle_size == 0 else cycle_size

    history = {}
    score = 0
    cycle = 0
    for _ in range(n_cycles):
        for _ in range(cycle_size):
            movement = True
            while movement:
                movement = False
                score = 0
                for i in range(1, n_lines - 1):
                    for j in range(1, n_cols - 1):
                        if lines[i][j] == "O":
                            if i > 0 and lines[i - 1][j] == '.':
                                lines[i - 1][j] = "O"
                                lines[i][j] = "."
                                movement = True
                            score = score + lines[i][0] + lines[0][j]
            
            lines = transpose(lines)
        
        cycle += 1
        cycle_hash = hash(''.join([''.join(l[1:-1]) for l in lines[1:-1]]))
        if cycle_hash in history.keys():
            cycle_start = history[cycle_hash][0]
            cycle_length = cycle - cycle_start

            n_loops = (n_cycles - cycle_start) // cycle_length
            n_cycles_required = n_cycles - n_loops * cycle_length

            for i, score in history.values():
                if i == n_cycles_required:
                    return score, [l[1:-1] for l in lines[1:-1]]
            
            raise Exception("")
        else:
            history[cycle_hash] = (cycle, score)

    return score, [l[1:-1] for l in lines[1:-1]]

print("example 1:", cycle("example1.txt", 1, 1)[0])
print("part 1:", cycle("input.txt", 1, 1)[0])
print("")

_, lines = cycle("example1.txt", 1)
if lines != input("example1-cycle1.txt"):
    raise Exception("Sanity check error.")

_, lines = cycle("example1.txt", 2)
if lines != input("example1-cycle2.txt"):
    raise Exception("Sanity check error.")

_, lines = cycle("example1.txt", 3)
if lines != input("example1-cycle3.txt"):
    raise Exception("Sanity check error.")

print("example 2:", cycle("example1.txt")[0])
print("part 2:", cycle("input.txt")[0])