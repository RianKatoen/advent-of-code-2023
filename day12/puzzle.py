import re
from typing import Generator
import math

def input(file: str) -> list[tuple[str, str]]:
    with open(file, "r") as input:
        return([tuple(line.strip().split(' ')) for line in input])

def get_options(line: str, max_hash: int, hash_count: int, q_count: int) -> Generator[tuple[int, int, str], None, None]:
    if len(line) == 0:
        yield (hash_count, q_count, line)
    elif hash_count == max_hash:
        yield (hash_count, q_count, line)
    elif hash_count < max_hash and q_count + hash_count >= max_hash:
        q_ix = line.find('?')
        for hc2, qc2, o in get_options(line[(q_ix + 1):], max_hash, hash_count, q_count - 1):
            yield (hc2, qc2, line[0:q_ix] + '.' + o)
        
        for hc2, qc2, o in get_options(line[(q_ix + 1):], max_hash, hash_count + 1, q_count - 1):
            yield (hc2, qc2, line[0:q_ix] + '#' + o)

def get_springs(line: str) -> list[int]:
    return([int(i) for i in line.split(',')])

def part1(file: str) -> int:
    n_legit_setups = 0
    pattern = re.compile(r'(?<!#)(#+)(?!#)')
    info = ((get_options(o, sum(get_springs(s)), o.count('#'), o.count('?')), get_springs(s)) for o, s in input(file))    

    for options, springs in info:
        for _, _, o in options:
            locs = pattern.findall(o)
            if len(locs) == len(springs) and all(len(l) == s for l, s in zip(locs, springs)):
                n_legit_setups += 1

    return n_legit_setups



def calculate_options(options: list[str], springs: list[int]) -> int:    
    if len(options) == len(springs):
        n_options = []
        for o, s in zip(options, springs):
            n_options.append(sum(1 for _ in get_spring_options(o, s, o.count('#'), o.count('?'))))
        return 0 if len(n_options) == 0 else math.prod(n_options)
    
    n_options = 0
    if len(options) > len(springs):     
        if options[0].count('#') == 0:
            skipperino = calculate_options(options[1:], springs)
            n_options = skipperino if skipperino > 0 else 0
            
    o_ix = 0
    s_ix = 0    
    while o_ix < len(options) and s_ix < len(springs):
        o, s = options[o_ix], springs[s_ix]
        print(s, o)
        # if o.count('#') >= s:
        #     i, new_o = 0, ''
        #     while i < len(o) and new_o.count('#') < s and (len(new_o) < s + 1  or o[i] != '#'):
        #         new_o += o[i]
        #         i += 1 
                      
        #     options.insert(o_ix, o[0:i])
        #     options[o_ix + 1] = o[i:]
        # else:
        spring_options = [x for x in get_spring_options(o, s)]

        if len(spring_options) == 0:
            print("wut")
            o_ix += 1
        else:
            nn_options = 0
            for ss, qq, oo in spring_options:
                print("  ", ss, qq, oo)
                q_ix = oo.find('?')
                if q_ix == -1:
                    no_more = calculate_options(options[(o_ix + 1):], springs[(s_ix + 1):])
                    # print("no_more:", no_more)
                    nn_options += no_more
                else:
                    new_option = oo[(q_ix + 1):] # skip one since that should be a . instead of questionmark.
                    # print("    ", ss, qq, oo, q_ix, new_option)
                    if len(new_option) > 0:
                        recursive_options = calculate_options([new_option] + options[(o_ix + 1):], springs[(s_ix + 1):])
                        nn_options += recursive_options
                    else:
                        nn_options += calculate_options(options[(o_ix + 1):], springs[(s_ix + 1):])

            o_ix += 1
            s_ix += 1

            n_options = (1 if n_options == 0 else n_options) * (1 if nn_options == 0 else nn_options)

    return n_options

def part2(file: str) -> int:
    options = 0
    for options, springs in [input(file)[2]]:
        # options = [o for o in (options + '?' + options + '?' + options + '?' + options + '?' + options).split('.') if o != '']
        # springs = [int(s) for s in (springs + ',' + springs + ',' + springs + ',' + springs + ',' + springs).split(',')]

        options = [o for o in options.split('.') if o != '']
        springs = [int(s) for s in springs.split(',')]

        print(calculate_options(options, springs))

    return options

#print("example 2:", part2("example1.txt"))
#print("wut:", calculate_options(['?###????????'], [3, 2, 1]))
def get_spring_options(line: str, spring: int, n_hash: int = 0, total_hashes: int = 0, prev: str = '') -> Generator[tuple[int, str], None, None]:   
    if spring == n_hash:
        yield (n_hash, line)
        return
    
    if total_hashes > spring or line == '':
        return
    
    if line[0] == '#' or line[0] == '?':
        for hc, l in get_spring_options(line[1:], spring, n_hash + 1, total_hashes + 1, line[0]):
            yield (hc, '#' + l)
    
    if line[0] == '?':
        for hc, l in get_spring_options(line[1:], spring, 0, total_hashes, line[0]):
            yield (hc, '.' + l)

def combinations(options: list[str], springs: list[int], n_options: int = 0, depth: int = 0) -> int:
    if len(springs) == 0:
        if sum([o.count('#') for o in options]) == 0:
            return n_options
        else:
            return 0
    
    if len(options) == 0:
        return 0
    
    o, s, nn_options = options[0], springs[0], 0
    print("  " * depth, s, o, options, springs, n_options)
    nn_options = 1
    for nh, oo in get_spring_options(o, s):
        if depth == 0:
            print(nh, oo)
    
        q_ix = oo.find('?')
        if q_ix >= 0 and q_ix < len(oo) - 1:
            if len(options) >= 1 and len(springs) > 1:
                nn_options += combinations([oo[(q_ix + 1):]] + options[1:], springs[1:], 1, depth + 1)
            else:
                nn_options += 1
        else:
            if nh != s:
                nn_options += combinations(options[1:], springs, 1, depth + 1)
            elif len(options) > 1 and len(springs) > 1:
                nn_options += combinations(options[1:], springs[1:], 1, depth + 1)
            else:
                nn_options += 1
    
    return n_options + nn_options

for g in get_spring_options('????', 1):
    print(g)

print("")
# print([i for i in get_spring_options('?', 1)])

for options, springs in input("example1.txt"):
    # options = [o for o in options.split('.') if o != '']
    # springs = [int(s) for s in springs.split(',')]

    options = [o for o in (options + '?' + options + '?' + options + '?' + options + '?' + options).split('.') if o != '']
    springs = [int(s) for s in (springs + ',' + springs + ',' + springs + ',' + springs + ',' + springs).split(',')]

    print(options, springs)
    print("combinations: ", combinations(options, springs))
    print("")