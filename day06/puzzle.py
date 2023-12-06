import math

def input(file: str) -> tuple[list[int], list[list[tuple[tuple[int, int, int], tuple[int, int, int]]]]]:
    if file == "example1.txt":
        return [(7, 9), (15, 40), (30, 200)]
    else:
        return [(51, 222), (92, 2031), (68, 1126), (90, 1225)]
    
def part1(games: list[tuple[int, int]]):
    outcomes = []
    for t, d in games:
        low_solution = int((t - math.sqrt(t * t - 4 * d)) / 2 + 1)
        high_solution = int((t + math.sqrt(t * t - 4 * d)) / 2)

        if (t - low_solution) * low_solution <= d:
            low_solution += 1
        
        if (t - high_solution) * high_solution <= d:
            high_solution -= 1

        outcomes.append(max(0, high_solution - low_solution + 1))

    total = 1
    for o in outcomes:
        total *= o

    return total


print("example 1:", part1(input("example1.txt")))
print("part 1:", part1(input("input.txt")))

def part2(games: list[tuple[int, int]]):
    time = ""
    distance = ""
    for t, d in games:
        time += f"{t}"
        distance += f"{d}"
    
    return(part1([(int(time), int(distance))]))

print("example 2:", part2(input("example1.txt")))
print("part 2:", part2(input("input.txt")))