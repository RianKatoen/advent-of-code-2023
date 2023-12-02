import re

def input(file: str) -> list[str]:
    lines = []
    with open(file, "r") as input:
        for line in input:
            stripped = re.sub(r'Game \d+:', "", line).strip()
            lines.append(stripped)
    return lines

def get_games(file):
    games = []
    colors = {
        'red': 0,
        'blue': 0,
        'green': 0
    }

    re_colors = {color: re.compile(r'(\d+) ' + color) for color in colors}
    gameNo = 1

    for game in input(file):
        colors = {
            'red': 0,
            'blue': 0,
            'green': 0
        }

        pulls = game.split(";")

        for pull in pulls:
            for color, re_color in re_colors.items():
                color_match = re_color.search(pull)
                if color_match:
                    colors[color] = max(colors[color], int(color_match.group(1)))

        games.append((gameNo, colors))
        gameNo += 1
    
    return games

def part1(file):
    threshold = { 'red': 12, 'green': 13, 'blue': 14 }
    result = 0
    for (gameNo, game) in get_games(file):
        valid = True
        for (color, no) in threshold.items():
            if game[color] > no:
                valid = False
        
        if valid:
            result += gameNo

    return result

def part2(file):
    result = 0
    for (gameNo, game) in get_games(file):
        result += game['red'] * game['blue'] * game['green']

    return result

print("example 1:", part1("example1.txt"))
print("part 1:", part1("input.txt"))

print("example 2:", part2("example1.txt"))
print("part 2:", part2("input.txt"))