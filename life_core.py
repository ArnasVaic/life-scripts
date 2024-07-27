import numpy as np
from scipy.signal import convolve2d

LIFE_KERNEL = [ [1, 1, 1], [1, 0, 1], [1, 1, 1] ]

def cycle_to_str(cycle, size, ascii):
  strings = []
  ascii_lookup = { 0: '-', 1: 'O' }

  for row in range(size):
    for i in range(len(cycle)):
      for col in range(size):
        cell_value = cycle[i][row][col]
        strings.append(ascii_lookup[cell_value] if ascii else f'{cell_value}')
        strings.append(' ')
      strings.append('  ')
    strings.append('\n')
  return ''.join(strings)

def life_next(current, torus_size):
    ncounts = convolve2d(current, LIFE_KERNEL, mode='same', boundary='wrap')
    result = np.zeros(current.shape)
    for i in range(torus_size):
        for j in range(torus_size):
            if ncounts[i, j] == 2:
                result[i, j] = current[i, j]
            elif ncounts[i, j] == 3:
                result[i, j] = 1
            else:
                result[i, j] = 0
    return result