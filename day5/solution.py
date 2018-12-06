import string

def is_reactive(a, b):
    return (a.upper() == b.upper()
    and ((a.isupper() and b.islower()) or (a.islower() and b.isupper())))

with open('input.txt', 'r') as f:
    line = f.readline().strip()

    # Part 1
    result = ['']
    for c in line:
        prev = result[-1]

        if is_reactive(prev, c):
            result.pop()
        else:
            result.append(c)

    # Remove the inert end caps
    print(len(''.join(result)))

    # Part 2
    min_polymer = len(line)
    for a in string.ascii_uppercase:
        result = ['']
        for c in line:
            if c.upper() != a:
                prev = result[-1]

                if is_reactive(prev, c):
                    result.pop()
                else:
                    result.append(c)
        min_polymer = min(min_polymer, len(''.join(result)))

    print(min_polymer)
