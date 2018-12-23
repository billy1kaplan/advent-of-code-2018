import re
from pprint import pprint

with open('input.txt', 'r') as f:
    state = f.readline().strip('initial state: ').strip()
    f.readline()
    rules = {}
    for line in f.readlines():
        pattern, result = line.strip().split(' => ')
        rules[pattern] = result

def advance(pattern, rules, start):
    if '#' in pattern[:3]:
        start += 3
        pattern = '...' + pattern
    if '#' in pattern[-3:]:
        pattern += '...'

    result = [c for c in pattern]
    for i in range(len(pattern)):
        window = pattern[i:i+5]
        if window in rules:
            result[i+2] = rules[window]
        elif i + 2 < len(result):
            result[i+2] = '.'
    return (''.join(result), start)

def sum_pots(cur_state, count):
    pot_sum = 0
    for i, pot in enumerate(cur_state):
        if pot == '#':
            pot_sum += i - count
    return pot_sum

cur_state = state
count = 0
results = []
for _ in range(20):
    cur_state, count = advance(cur_state, rules, count)
print('Part 1: ', sum_pots(cur_state, count))

# Empirically determined
def compute(i):
   return 33055 + (i - 1000) * 33 
print('Part 2: ', compute(50000000000))
