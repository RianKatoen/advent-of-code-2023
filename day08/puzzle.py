import re, math

def input(file: str) -> tuple[list[int], dict[str, tuple[str, str]]]:
    pattern = re.compile(r'([0-9,A-Z]{3}) = \(([0-9,A-Z]{3}), ([0-9,A-Z]{3})\)')
    moves, instructions = [], {}

    with open(file, "r") as input:
        for line in (l.strip() for l in input):
            if line == "":
                continue
            elif len(moves) == 0:
                moves = [0 if c == 'L' else 1 for c in line]
            else:
                search = pattern.search(line)
                if search:
                    instructions[search.group(1)] = (search.group(2), search.group(3))

    return (moves, instructions)

def part1(file: str):
    current_pos = 'AAA'
    moves, instructions = input(file)
    n_moves = 0
    while True:
        for move in moves:
            n_moves +=1
            current_pos = instructions[current_pos][move]
            if current_pos == 'ZZZ':
                return n_moves

print("example 1:", part1("example1.txt"))
print("example 2:", part1("example2.txt"))
print("part 1:", part1("input.txt"))

def get_loops(file: str):
    moves, instructions = input(file)
    positions = [p for p in instructions.keys() if p[2] == 'A']
    loops, paths = [], []

    for pos in positions:
        n_move, i, is_loop, loop, path = 0, 0, False, {}, []
        while not is_loop:
            i = 0
            for move in moves:
                i += 1
                n_move += 1
                path.append(pos)
                pos = instructions[pos][move]
                if pos[2] == 'Z':
                    if (i, pos) in loop.keys():
                        is_loop = True
                        break
                    else:
                        loop[(i, pos)] = n_move
                    
        loops.append(loop)
        paths.append(path)

    return loops, paths

# Through Inspection I noticed all loops ended on one-and-only-one tile, in the example it didn't.
# So I just used that to find the lowest integer multiplicator that made all the periods equal.
# Seems to be overkill tbh
def part2(file: str):
    loops, paths = get_loops(file)

    unique_denominators = []
    values = [[x for x in loop.values()][0] for loop in loops]
    while len(values) > 0:
        gcd = math.gcd(*values)
        new_values = []
        for val in values:
            if val != gcd and gcd > 1:
                new_values.append(val // gcd)
            else:
                unique_denominators.append(val)
                
        values = new_values

    result = 1 
    for d in unique_denominators:
        result *= d

    values = [[x for x in loop.values()][0] for loop in loops]
    gcd = math.gcd(*values)
    
    return gcd * result

print("example 3:", part2("example3.txt"))
print("part 2:", part2("input.txt"))