from enum import Enum

def input(file: str) -> list[str]:
    with open(file, "r") as input:
        return [line.strip() for line in input]
    
class Direction(Enum):
    NONE = (-9999, -9999)
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

def transform(location: tuple[int, int], direction: Direction) -> tuple[int, int]:
    return (location[0] + direction.value[0], location[1] + direction.value[1])

def move(location: tuple[int, int], direction: Direction, tile: str) -> tuple[tuple[tuple[int, int], Direction], tuple[tuple[int, int], Direction]]:
    direction_split = None

    if tile == '/':
        match direction:
            case Direction.RIGHT: direction = Direction.UP
            case Direction.LEFT: direction = Direction.DOWN
            case Direction.DOWN: direction = Direction.LEFT
            case Direction.UP: direction = Direction.RIGHT
    elif tile == '\\':
        match direction:
            case Direction.RIGHT: direction = Direction.DOWN
            case Direction.LEFT: direction = Direction.UP
            case Direction.DOWN: direction = Direction.RIGHT
            case Direction.UP: direction = Direction.LEFT
    elif tile == '-':
        match direction:
            case Direction.DOWN: direction, direction_split = Direction.LEFT,  Direction.RIGHT
            case Direction.UP: direction, direction_split = Direction.LEFT, Direction.RIGHT
    elif tile == '|':
        match direction:
            case Direction.LEFT: direction, direction_split = Direction.DOWN, Direction.UP
            case Direction.RIGHT: direction, direction_split = Direction.DOWN, Direction.UP

    return ((transform(location, direction), direction), (transform(location, direction_split), direction_split) if direction_split != None else ((-1, -1), Direction.NONE))


def traverse(location: tuple[int, int], direction: Direction, tiles: list[list[str]]) -> set[tuple[int, int]]:
    n_rows, n_cols = len(tiles), len(tiles[0])
    beams, all_beams, energized = set([(location, direction)]), set(), set()

    while len(beams) > 0:
        new_beams = set()
        for (row, col), direction in beams:
            all_beams.add(((row, col), direction))
            energized.add((row, col))
            ((row, col), direction), ((row2, col2), direction2) = move((row, col), direction, tiles[row][col])

            if row >= 0 and row < n_rows and col >= 0 and col < n_cols and ((row, col), direction) not in all_beams:
                new_beams.add(((row, col), direction))
            if row2 >= 0 and row2 < n_rows and col2 >= 0 and col2 < n_cols and ((row2, col2), direction2) not in all_beams:
                new_beams.add(((row2, col2), direction2))

            #print((row, col), direction)

        beams = new_beams

    return energized


def score(location: tuple[int, int], direction: Direction, tiles: list[list[str]]) -> int:
     return sum(1 for _ in traverse(location, direction, tiles))

def part1(file: str) -> int:
    map = input(file)
    return score((0, 0), Direction.RIGHT, map)

print("example 1:", part1("example1.txt"))
print("part 1:", part1("input.txt"))

print("")

def part2(file: str) -> int:
    map = input(file)
    n_rows, n_cols = len(map), len(map[0])

    scores = []
    for col in range(1, n_cols - 1):
        scores.append(score((0, col), Direction.DOWN, map))
        scores.append(score((n_rows - 1, col), Direction.UP, map))

    for row in range(1, n_rows - 1):
        scores.append(score((row, 0), Direction.RIGHT, map))
        scores.append(score((row, n_cols - 1), Direction.LEFT, map))

    scores.append(score((0, 0), Direction.RIGHT, map))
    scores.append(score((0, 0), Direction.DOWN, map))

    scores.append(score((n_rows - 1, 0), Direction.RIGHT, map))
    scores.append(score((n_rows - 1, 0), Direction.UP, map))

    scores.append(score((0, n_cols - 1), Direction.LEFT, map))
    scores.append(score((0, n_cols - 1), Direction.DOWN, map))

    scores.append(score((n_rows - 1, n_cols - 1), Direction.LEFT, map))
    scores.append(score((n_rows - 1, n_cols - 1), Direction.UP, map))

    return max(scores)

print("example 2:", part2("example1.txt"))
print("part 2:", part2("input.txt"))