import re

with open('input.txt', 'r') as f:
    lines = f.readlines()

    # Part 1:
    extract_str = re.compile(r'#(?P<id>\d+)\s@ (?P<x>\d+),(?P<y>\d+): (?P<width>\d+)x(?P<height>\d+)')

    def add_line(fabric, line):
        cut_region = extract_str.match(line)

        identifier = cut_region.group('id')

        x = int(cut_region.group('x')) - 1
        y = int(cut_region.group('y')) - 1

        width = int(cut_region.group('width'))
        height = int(cut_region.group('height'))

        for i in range(y, y + height):
            for j in range(x, x + width):
                fabric[i][j] += 1

    fabric = [[0] * 1000 for _ in range(1000)]
    for line in lines:
        add_line(fabric, line)
    print(len([pos for row in fabric for pos in row if pos > 1]))

    def is_non_overlapping(fabric, line):
        cut_region = extract_str.match(line)

        identifier = cut_region.group('id')

        x = int(cut_region.group('x')) - 1
        y = int(cut_region.group('y')) - 1

        width = int(cut_region.group('width'))
        height = int(cut_region.group('height'))

        for i in range(y, y + height):
            for j in range(x, x + width):
                if fabric[i][j] > 0:
                    return False
        print(f'Answer: {identifier}')
        return True

    # Part 2:
    for i in range(len(lines)):
        excluded = lines[i]
        excluding_one = lines[:i] + lines[i+1:]

        fabric = [[0] * 1000 for _ in range(1000)]

        for included_line in excluding_one:
            add_line(fabric, included_line)
        if is_non_overlapping(fabric, excluded): break
