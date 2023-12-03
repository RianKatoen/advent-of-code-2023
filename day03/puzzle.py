import re

def char_to_int(val: str) -> int:
    pattern = re.compile(r'\d{1}')
    if pattern.search(val):
        return int(val)
    elif val == '.':
        return -2
    else:
        return -1

# 0-9 is value
# -1 is symbol
# -2 is dot
def input(file: str) -> list[list[int]]:
    lines = [[char for char in line.strip()] for line in open(file, "r")]
    return lines


def create_info(matrix: list[list[int]]) -> tuple[int, int, dict[tuple[int, int], str], list[dict[tuple[int, int], int]]]:
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
            val=char_to_int(char)

            #number
            if val > 0:
                number=""
                k = j
                while k < n_columns and char_to_int(row[k]) >= 0:
                    number += row[k]
                    k += 1
                row_numbers[(j, k - 1)] = int(number)
                j = k
            #symbol
            elif val == -1:
                symbols[(i, j)] = char
                j += 1
            else:
                j += 1
        
        numbers.append(row_numbers)
        i += 1

    return(n_rows, n_columns, symbols, numbers)

def scan_row(col: int, numbers: dict[tuple[int, int], int]) -> dict[tuple[int, int], int]:
    valid_numbers: dict[tuple[int, int], int] = {} 
    for (col_start, col_end), number in numbers.items():
        if number == 617:
            print((col, (col_start, col_end), number))
            print(col_start - 1 <= col)
            print(col_end + 1 >= col)
            print("")

        if col_start - 1 <= col and col_end + 1 >= col:
            valid_numbers[(col_start, col_end)] = number
    
    # clear from look up list for faster lookups later on
    for pos in valid_numbers:
       numbers.pop(pos)
    
    return valid_numbers


def part1(file: str) -> int:
    n_rows, n_columns, symbols, numbers = create_info(input(file))
    
    for row in symbols.items():
        print(row)    

    print("")
    for number in numbers:
        print(number.items())

    print("")
    
    print("Symbols:", len(symbols), "; Numbers:", len(numbers))

    legit_numbers: list[dict[tuple[int, int], int]] = []
    for n_row in range(n_rows):
        legit_numbers.append({})

    for (row, col) in symbols:
        legit_numbers[row].update(scan_row(col, numbers[row]))
        if row > 0:
            legit_numbers[row - 1].update(scan_row(col, numbers[row - 1]))
        if row < n_rows:
            legit_numbers[row + 1].update(scan_row(col, numbers[row + 1]))

    print("")
    for number in legit_numbers:
        print(number.items())
    
    print("")
    for number in numbers:
        print(number.items())

    for number in legit_numbers:
        for x in number.values():
            print(x)

    return sum([sum(number.values()) for number in legit_numbers])

print("example 1:", part1("example.txt"))
print("part 1:", part1("input.txt"))