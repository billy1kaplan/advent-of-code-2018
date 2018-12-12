from functools import lru_cache

serial_n = 5535

@lru_cache(maxsize = 90000)
def compute_square_power(x, y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_n
    power_level *= rack_id
    hundreds_only = (power_level // 100) % 10
    return hundreds_only - 5

def square_n(i, j, n):
    for x in range(n):
        for y in range(n):
            yield (i + x, j + y)

def compute_power(i, j, size):
    return sum([compute_square_power(x, y) for x, y in square_n(i, j, size)])

grid_size = 300
max_power = 0
loc = None
count = 0
for size in range(1, 300):
    for i in range(grid_size - size - 1):
        for j in range(grid_size - size - 1):
            count += 1
            power = compute_power(i, j, size)
            if power > max_power:
                max_power = power
                loc = (i, j, size)

print(loc, max_power)
