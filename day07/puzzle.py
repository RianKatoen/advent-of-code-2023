import re
from enum import IntEnum

def value(char: str):
    pattern = re.compile('\d')
    search = pattern.search(char)
    if search:
        return int(char)
    else:
        match char:
            case 'T': return 10
            case 'J': return 11
            case 'Q': return 12
            case 'K': return 13
            case 'A': return 14

def input(file: str) -> tuple[int, list[int], list[int]]:
    lines = []
    with open(file, "r") as input:
        for line in input:
            cards, bid = line.strip().split(' ')
            values = [value(c) for c in cards]
            values_sorted = [value(c) for c in cards]
            values_sorted.sort()
            lines.append((int(bid), values, values_sorted))
    return lines


class Hand(IntEnum):
    NONE = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 8
    FIVE_OF_A_KIND = 16

def determine_hand(cards_sorted: list[int]):
    hands = []
    hand_value, hand = cards_sorted[0], Hand.HIGH_CARD
    for card in cards_sorted[1:]:
        if card == hand_value:
            hand = Hand(hand << 1)
            continue 
        else:
            hands.append((hand_value, hand))
            hand_value, hand = card, Hand.HIGH_CARD
    
    hands.append((hand_value, hand))
    hand_types = [h for _, h in hands]

    if Hand.ONE_PAIR in hand_types and Hand.THREE_OF_A_KIND in hand_types:
        return (Hand.FULL_HOUSE, hands)
    if hand_types.count(Hand.ONE_PAIR) == 2:
        return (Hand.TWO_PAIR, hands)
    else:
        return (Hand(max([int(h) for _, h in hands])), hands)

def rule_2(card1: list[int], card2: list[int]):
    for c1, c2 in zip(card1, card2):
        if c1 > c2:
            return 1
        if c2 > c1:
            return 2

def part1(file: str) -> int:
    games = input(file)
    hands = []
    for bid, cards, cards_sorted in games:
        hand, _ = determine_hand(cards_sorted)
        hands.append((hand, bid, cards))

    hands.sort(key = lambda h: (h[0], h[2][0], h[2][1], h[2][2], h[2][3], h[2][4]))
    return(sum([(i + 1) * bid for i, (_, bid, _) in zip(range(len(hands)), hands)]))

print("example 1:", part1("example1.txt"))
print("part 1:", part1("input.txt"))