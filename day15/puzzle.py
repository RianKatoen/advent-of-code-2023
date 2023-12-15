import re

def input(file: str) -> list[str]:
    with open(file, "r") as input:
        return [line.strip().split(',') for line in input][0]

def hash(string: str):
    value = 0
    for c in string:
        value += ord(c)
        value *= 17
        value %= 256

    return value

def part1(file: str) -> int:
    total = 0
    for string in input(file):
        total += hash(string)
    return total

print("example 1:", part1("example1.txt"))
print("part 1:", part1("input.txt"))
print("")

def part2(file: str) -> int:
    boxes: list[list[tuple[str. int]]] = [[] for _ in range(0, 256)]

    label_search_operation = re.compile(r'([a-z]+)[=|-]')
    is_equal_operation = re.compile(r'([a-z]+)[=](\d+)')

    for string in input(file):
        label = label_search_operation.search(string).group(1)
        box = boxes[hash(label)]

        search = is_equal_operation.search(string)
        if search:
            focal_length = int(search.group(2))

            found = False
            for i in range(0, len(box)):
                search_label, _ = box[i]
                if label == search_label:
                    box[i] = (label, focal_length)
                    found = True 
                    break
            
            if not found:
                box.append((label, focal_length))

        else:
            for i in range(0, len(box)):
                search_label, focal_length = box[i]
                if label == search_label:
                    box.pop(i)
                    break

    score = 0
    for i, box in zip(range(0, 256), boxes):
        for slot, (_, focal_length) in zip(range(1, len(box) + 1), box):
            score += (1 + i) * slot * focal_length
    
    return score

print("example 2:", part2("example1.txt"))
print("part 2:", part2("input.txt"))