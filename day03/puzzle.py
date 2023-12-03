import re

def input(file: str) -> list[list[str]]:
    return [[char for char in line.strip()] for line in open(file, "r")]

# create two list containing the dictionary of unique symbols and a row-by-row list of number interval.
def create_info(matrix: list[list[int]]) -> tuple[int, int, dict[tuple[int, int], str], list[dict[tuple[int, int], int]]]:
    pattern = re.compile(r'\d{1}')
    symbols={}
    numbers=[]

    n_rows=len(matrix)
    n_columns=len(matrix[0])

    i = 0
    while i < n_rows:
        row=matrix[i]
        row_numbers={}
        
        j = 0
        while j < n_columns:
            char=row[j]

            #number
            if pattern.search(char):
                number=""
                k = j
                while k < n_columns and pattern.search(row[k]):
                    number += row[k]
                    k += 1
                row_numbers[(j, k - 1)] = int(number)
                j = k
            #symbol or number
            else:
                if char != '.':
                    symbols[(i, j)] = char
                j += 1
        
        numbers.append(row_numbers)
        i += 1

    return(symbols, numbers)

def scan_row(col: int, numbers: dict[tuple[int, int], int], pop_entries: bool = True) -> dict[tuple[int, int], int]:
    valid_numbers: dict[tuple[int, int], int] = {} 
    for (col_start, col_end), number in numbers.items():
        # substract 1 and add 1 to account for diagonals.
        if col_start - 1 <= col and col_end + 1 >= col:
            valid_numbers[(col_start, col_end)] = number
    
    # Optionally clear from look up list for faster lookups later on
    if pop_entries:
        for pos in valid_numbers:
            numbers.pop(pos)
    
    return valid_numbers

def find_parts(symbols: dict[tuple[int, int], str], numbers: list[dict[tuple[int, int], int]], pop_entries: bool = True) -> list[dict[tuple[int, int], int]]:
    n_rows=len(numbers)
    legit_numbers: list[dict[tuple[int, int], int]] = [{} for _ in range(n_rows)]
    for (row, col) in symbols:
        legit_numbers[row].update(scan_row(col, numbers[row], pop_entries))
        if row > 0:
            legit_numbers[row - 1].update(scan_row(col, numbers[row - 1], pop_entries))
        if row < n_rows:
            legit_numbers[row + 1].update(scan_row(col, numbers[row + 1], pop_entries))
    
    return legit_numbers

def part1(file: str) -> int:
    legit_numbers = find_parts(*create_info(input(file)))
    return sum([sum(number.values()) for number in legit_numbers])

def part2(file: str) -> int:
    symbols, numbers = create_info(input(file))

    gear_ratios = 0
    gears = { pos:symbol for pos, symbol in symbols.items() if symbol == "*" }
    for (pos, gear) in gears.items():
        # this feels stupid but I don't understand python well enough to use proper syntax
        legit_numbers = []
        for part in find_parts({pos: gear}, numbers, False):
            for val in part.values():
                legit_numbers.append(val)

        if len(legit_numbers) == 2:
            gear_ratios += legit_numbers[0] * legit_numbers[1]

    return gear_ratios

print("example 1:", part1("example.txt"))
print("part 1:", part1("input.txt"))

print("example 2:", part2("example.txt"))
print("part 2:", part2("input.txt"))