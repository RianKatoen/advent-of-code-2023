import re

def input(file: str) -> list[tuple[set[int], set[int]]]:
    lines = []
    with open(file, "r") as input:
        for line in input:
            stripped = re.sub(r'Card\s+\d+:\s+', "", line.strip())
            stripped = re.split(r'\s+\|\s+', stripped)
            stripped = [re.split(r'\s+', x) for x in stripped]

            lines.append([{int(y) for y in x} for x in stripped])
    return lines

def score(card: tuple[set[int], set[int]]) -> int:
    matches = 0
    winning, numbers = card
    for number in numbers:
        if number in winning:
            matches += 1
    
    return matches

def part1(file: str) -> int:
    scores = [score(card) for card in input(file)]
    return sum([0 if score == 0 else 1 << (score - 1) for score in scores])

def part2(file: str):
    scores = [score(card) for card in input(file)]
    n_cards = len(scores)

    # create list of what cards you would win.
    scores = [[x for x in range(ix + 1, ix + score + 1)] for ix, score in zip(range(n_cards), scores)]
    cards = [1 for _ in range(n_cards)]
    round = {c:1 for c in range(n_cards)}

    no_round = 1
    while len(round.keys()) > 0:
        print(no_round)
        new_round = {c:0 for c in range(n_cards)}
        for card in round:
            new_cards = scores[card]
            for new_card in new_cards:
                cards[new_card] += 1
                new_round[new_card] += 1

        round = new_round
        no_round+=1

    return sum(cards)

print("example 1:", part1("example1.txt"))
print("part 1:", part1("input.txt"))

print("example 2:", part2("example1.txt"))
print("part 2:", part2("input.txt"))