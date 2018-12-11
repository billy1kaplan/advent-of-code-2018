import re
from pprint import pprint

with open('input.txt', 'r') as f:
    lines = f.readlines()

digits = re.compile(r'[-]?\d+')
def number_extractor(line):
    str_numbers = re.findall(digits, line)
    return list(map(int, str_numbers))

def get_x(point):
    x, _, _, _ = point
    return x

def get_y(point):
    _, y, _, _ = point
    return y

def get_x_vel(point):
    _, _, x_vel, _ = point
    return x_vel

def get_y_vel(point):
    _, _, _, y_vel = point
    return y_vel

def update_point(point):
    x, y, x_vel, y_vel = point
    return (x + x_vel, y + y_vel, x_vel, y_vel)

def update_all_points(points):
   return [update_point(point) for point in points]

def display_points(points, time):
    min_x = min([get_x(point) for point in points])
    min_y = min([get_y(point) for point in points])
    max_x = max([get_x(point) for point in points])
    max_y = max([get_y(point) for point in points]) 
    x_diff = max_x - min_x + 1
    y_diff = max_y - min_y + 1
    # Look for when the stars align
    if x_diff < 80 and y_diff < 30:
        stars = [['.' for _ in range(x_diff)] for _ in range(y_diff)]
        for x, y, _, _ in points:
            stars[y - min_y][x - min_x] = '#'
        print('\n\n')
        print(f'MESSAGE AT: {time} seconds')
        for line in stars:
            print(''.join(line))

points = [number_extractor(line) for line in lines]
time = 0
for _ in range(100000):
    display_points(points, time)
    points = update_all_points(points)
    time += 1

display_points(points)
