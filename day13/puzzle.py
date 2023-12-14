def input(file: str) -> list[tuple[int, int, list[list[str]]]]:
    rock_formations = []
    with open(file, "r") as input:
        rock_formation = []
        for line in (l.strip() for l in input):
            if line == '':
                rock_formations.append((len(rock_formation), len(rock_formation[0]), rock_formation))
                rock_formation = []
            else:
                rock_formation.append(line)

    return rock_formations
def transpose(rocks: list[list[str]]) -> tuple[int, int, list[list[str]]]:
    new_rocks = []
    n_rows, n_cols = len(rocks), len(rocks[0])

    
    for j in range(n_cols):
        new_rock_line = []
        new_rocks.append(new_rock_line)
        for i in range(n_rows):    
            new_rock_line.append(rocks[i][j])
    
    return n_cols, n_rows, new_rocks

def part1(file: str) -> int:
    total_score = 0
    for n_rows, _, rock_formation in input(file):
        scores = []
        offset = 100
        for _ in range(2):
            for row in range(1, n_rows):
                length = min(row, n_rows - row)
                if rock_formation[(row - length):row] == rock_formation[row:(row + length)][::-1]:
                    scores.append(offset * row)
            
            n_rows, _, rock_formation = transpose(rock_formation)
            offset = 1
        
        if len(scores) > 0:
            total_score += max(scores)
    
    return total_score

print("example 1:", part1("example1.txt"))
print("part 1:", part1("input.txt"))