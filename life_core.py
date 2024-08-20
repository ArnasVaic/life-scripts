import numpy as np
from scipy.signal import convolve2d

LIFE_KERNEL = [ [1, 1, 1], [1, 0, 1], [1, 1, 1] ]

def find_cycle(frame):
  cycle, current = [frame], frame
  while True:
    current = next(current)
    if np.array_equal(current, cycle[0]):
      break
    cycle.append(current)
  return cycle

def display(frame):
  ascii_lookup = { 0: '-', 1: 'O' }
  strings = []
  for row in range(frame.shape[0]):
    for col in range(frame.shape[1]):
      strings.append(ascii_lookup[frame[row][col]])
      strings.append(' ')
    strings.append('\n')
  return ''.join(strings)

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

def next(frame):
    ncounts = convolve2d(frame, LIFE_KERNEL, mode='same', boundary='wrap')
    result = np.zeros(frame.shape)
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            if ncounts[i, j] == 2:
                result[i, j] = frame[i, j]
            elif ncounts[i, j] == 3:
                result[i, j] = 1
            else:
                result[i, j] = 0
    return result