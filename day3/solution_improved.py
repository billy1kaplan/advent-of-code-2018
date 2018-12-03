import re

with open('input.txt', 'r') as f:
    lines = [list(map(int, re.findall(r'\d+', line))) for line in f.readlines()]

    # Part 1:
    def add_line(fabric, line):
        identifier, x, y, width, height = line

        for i in range(y, y + height):
            for j in range(x, x + width):
                fabric[i][j] += 1

    def count():
        count = 0
        for i in range(len(fabric)):
            for j in range(len(fabric[0])):
                if fabric[i][j] > 1:
                    count += 1
        return count

    fabric = [[0] * 1000 for _ in range(1000)]

    for line in lines:
        add_line(fabric, line)
    print(count())

    # Part 2:
    for line in lines:
        identifier, x, y, width, height = line

        def all_one():
            for i in range(y, y + height):
                for j in range(x, x + width):
                    if not fabric[i][j] == 1:
                        return False
            return True

        if all_one():
            print(f'Non-overlapping: {identifier}')
            break
