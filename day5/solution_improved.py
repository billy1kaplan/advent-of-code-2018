import string

def is_reactive(a, b):
    return (a.upper() == b.upper()
    and ((a.isupper() and b.islower()) or (a.islower() and b.isupper())))

def react_polymer(polymer):
    result = ['']
    for c in line:
        prev = result[-1]

        if is_reactive(prev, c):
            result.pop()
        else:
            result.append(c)
    return ''.join(result)

with open('input.txt', 'r') as f:
    line = f.readline().strip()

    # Part 1
    # Remove the inert end caps
    print(len(react_polymer(line)))

    # Part 2
    min_polymer = len(line)
    for cur_char in string.ascii_uppercase:
        polymer_removed = ''.join([c for c in line if not c.upper() == cur_char])
        length = len(react_polymer(polymer_removed))
        print(len(polymer_removed), length)
        min_polymer = min(min_polymer, length)
    print(min_polymer)
