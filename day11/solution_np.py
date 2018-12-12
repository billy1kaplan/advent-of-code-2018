import numpy as np

serial_n = 5535

def compute_fuel_cell(x, y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_n
    power_level *= rack_id
    hundreds_only = (power_level // 100) % 10
    return hundreds_only - 5

grid_size = 300
grid_shape = (grid_size, grid_size)

fuel_grid = np.fromfunction(compute_fuel_cell, grid_shape)
def maximize_power(sub_size):
    print(sub_size) # To track progress, this is still slow!
    sub_shape = (sub_size, sub_size)

    sub_grid_size = grid_size - sub_size + 1
    sub_grid = (sub_grid_size, sub_grid_size)

    view_shape = tuple(np.subtract(fuel_grid.shape, sub_shape) + 1) + sub_shape
    strides = fuel_grid.strides + fuel_grid.strides
    sub_matrices = np.lib.stride_tricks.as_strided(fuel_grid, view_shape, strides)
    sub_matrix_sums = np.einsum('ijkl->ij', sub_matrices)
    max_sum_loc, max_power = np.argmax(sub_matrix_sums), np.max(sub_matrix_sums)
    x, y =  np.unravel_index(max_sum_loc, sub_grid)
    return (x, y, max_power, sub_size)

powers = [maximize_power(g) for g in range(1, 300)]
best = sorted(powers, key = lambda x: x[2])[-1]
x, y, _, s = best
print(f'{x},{y},{s}')
