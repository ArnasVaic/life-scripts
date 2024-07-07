# %%
from cycle import read_pretty_cycle_data
import numpy as np

def is_cut_off(i, j, N):
    return i >= N or j >= N

def compute_cost(x, y, config, N, alpha, beta):
    M = config.shape[0]
    cut_off_penalty = 0
    for i in range(M):
        for j in range(M):
            if config[i, j] == 1 and is_cut_off((x + i) % N, (y + j) % N, N):
                cut_off_penalty += 1
    center_x = x + M / 2
    center_y = y + M / 2
    centering_penalty = ((center_x / N) - 0.5) ** 2 + ((center_y / N) - 0.5) ** 2
    return alpha * cut_off_penalty + beta * centering_penalty

def find_best_offset(config, N, alpha=1.0, beta=1.0):
    M = config.shape[0]
    min_cost = float('inf')
    best_offset = (0, 0)
    for x in range(N):
        for y in range(N):
            cost = compute_cost(x, y, config, N, alpha, beta)
            if cost < min_cost:
                min_cost = cost
                best_offset = (x, y)
    return best_offset

with open('test/pretty/input.txt') as input:
    frame = read_pretty_cycle_data(input, 8, 'O', '-', ' ')

    (dx, dy) = find_best_offset(frame, 8)

    print(np.roll(frame, shift=(dx, dy), axis=(0, 1)))

# %%
