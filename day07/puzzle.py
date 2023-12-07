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
    if len(cards_sorted) == 0:
        return (Hand.NONE, hands)
    
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

def part2(file: str) -> int:
    games = input(file)
    games = [(bid, [c if c != 11 else 1 for c in cards], [c for c in cards_sorted if c != 11], cards.count(11)) for bid, cards, cards_sorted in games]

    hands = []
    for bid, cards, cards_sorted, n_jokers in games:
        hand, _ = determine_hand(cards_sorted)
        if n_jokers == 0:
            hands.append((hand, bid, cards))
        elif n_jokers == 5:
            hands.append((Hand.FIVE_OF_A_KIND, bid, cards))
        elif n_jokers == 4:
            hands.append((Hand.FIVE_OF_A_KIND, bid, cards))
        elif n_jokers == 3:
            if hand == Hand.ONE_PAIR:
                hands.append((Hand.FIVE_OF_A_KIND, bid, cards))
            else:
                hands.append((Hand.FOUR_OF_A_KIND, bid, cards))
        elif n_jokers == 2:
            if hand == Hand.THREE_OF_A_KIND:
                hands.append((Hand.FIVE_OF_A_KIND, bid, cards))
            elif hand == Hand.ONE_PAIR:
                hands.append((Hand.FOUR_OF_A_KIND, bid, cards))
            else:
                hands.append((Hand.THREE_OF_A_KIND, bid, cards))
        elif n_jokers == 1:
            if hand == Hand.FOUR_OF_A_KIND:
                hands.append((Hand.FIVE_OF_A_KIND, bid, cards))
            elif hand == Hand.THREE_OF_A_KIND:
                hands.append((Hand.FOUR_OF_A_KIND, bid, cards))
            elif hand == Hand.TWO_PAIR:
                hands.append((Hand.FULL_HOUSE, bid, cards))
            elif hand == Hand.ONE_PAIR:
                hands.append((Hand.THREE_OF_A_KIND, bid, cards))
            else:
                hands.append((Hand.ONE_PAIR, bid, cards))
    
    hands.sort(key = lambda h: (h[0], h[2][0], h[2][1], h[2][2], h[2][3], h[2][4]))
    return(sum([(i + 1) * bid for i, (_, bid, _) in zip(range(len(hands)), hands)]))

print("example 2:", part2("example1.txt"))
print("part 2:", part2("input.txt"))