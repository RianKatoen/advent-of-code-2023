def input(file: str) -> tuple[list[int], dict[str, tuple[str, str]]]:
    with open(file, "r") as input:
            return([[int(i) for i in line.strip().split(' ')] for line in input])

def get_difference(x: list[int]) -> list[int]:
     return([x[i + 1] - x[i] for i in range(len(x) - 1)])

def get_differences(X: list[int]) -> list[list[int]]:
    differences = []
    while not all([x == 0 for x in X]):
        differences.append(X)
        X = get_difference(X)
    
    return differences

def part1(file: str):
    histories = input(file)
    differences = [get_differences(h) for h in histories]

    for difference in differences:
        delta = 0
        for history in difference[::-1]:
             delta += history[-1]
             history.append(delta)
    
    return sum([h[0][-1] for h in differences])

print("example1:", part1("example1.txt"))
print("part1:", part1("input.txt"))
    
def part2(file: str):
    histories = input(file)
    differences = [get_differences(h) for h in histories]
    differences = [[h[::-1] for h in d] for d in differences]

    for difference in differences:
        delta = 0
        for history in difference[::-1]:
             delta = history[-1] - delta
             history.append(delta)
    
    return sum([h[0][-1] for h in differences])

print("example2:", part2("example1.txt"))
print("part2:", part2("input.txt"))