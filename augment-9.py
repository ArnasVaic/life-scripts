# %%
import numpy as np
import re

from utils import pretty_fraction
import life_io as lio
import life_core as lc
import life_utils as lu
import life_misc as sp

TORUS_SIZE = 9
input_filename = f'Torus{TORUS_SIZE}x{TORUS_SIZE}.txt'
output_filename = f'Torus{TORUS_SIZE}x{TORUS_SIZE}-v1.txt'
evrd_filename = f'EvRelativeDiffsT{TORUS_SIZE}x{TORUS_SIZE}.txt'

# read and store file in memory
configurations = {}

def dfs_mark_island(frame, x, y):

    if x < 0 or x >= frame.shape[0] or y < 0 or y >= frame.shape[1] or frame[x, y] == 0:
        return
    
    # Recursively erase the island
    frame[x, y] = 0

    adj_coords = [ (x, y) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
    [dfs_mark_island(frame, *coord) for coord in adj_coords]
    
def count_islands(frame):
    if frame.size == 0:
        return 0
    
    frame_copy = frame.copy()
    
    island_count = 0
    
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):

            if frame_copy[i, j] != 1:
                continue

            # We found a cell that has not been erased
            # means it's going to be a new island.
            
            island_count += 1
            dfs_mark_island(frame_copy, i, j)

    return island_count
                    
with open(input_filename) as input, \
    open(evrd_filename) as evrd_input, \
    open(output_filename, 'w') as output:
    
    toruses_read = 0

    while True:

        print(f'Number of toruses read: {toruses_read}')
        toruses_read = toruses_read + 1

        # read the configuration (4 + N lines per configuration)
        config_line, decays_line, rates_line = input.readline(), input.readline(), input.readline()

        if not config_line:
            break

        frame_lines = [input.readline() for _ in range(TORUS_SIZE)]
        frame = lio.parse_pretty_frame(''.join(frame_lines), TORUS_SIZE, 'O', '-', ' ')
        empty_line = input.readline()
        pretty_frame = lu.find_pretty(frame)

        cycle = [frame]

        current = frame
        while True:
            current = lc.life_next(current, TORUS_SIZE)
            if np.array_equal(current, cycle[0]):
                break
            cycle.append(current)

        # new relative differnce between first and second eigen values
        evrd = evrd_input.readline().strip()

        # parse config line
        id = int(re.search(r'#(\d+)', config_line).group(1))
        period = int(re.search(r'c(\d+)', config_line).group(1))

        param_c = pretty_fraction(sum([f.sum() for f in cycle]), period)
        param_h = pretty_fraction(sum([sp.calculate_param_h(f) for f in cycle]), period)
        param_d = pretty_fraction(sum([sp.calculate_param_d(f) for f in cycle]), period)

        param_hh = pretty_fraction(sum([sp.calculate_param_h(f, 2) for f in cycle]), period)
        param_dd = pretty_fraction(sum([sp.calculate_param_d(f, 2) for f in cycle]), period)
        param_hd = pretty_fraction(sum([sp.calculate_param_hd(f) for f in cycle]), period)

        # output new config line
        configurations[id] = {
            "special_params": {
                "p": period,
                "c": param_c,
                "h": param_h,
                "d": param_d,
                "hh": param_hh,
                "dd": param_dd,
                "hd": param_hd
            },
            "evrd": evrd,
            "pretty-frame": pretty_frame
        }

        # output.write(f'#{id}: [{period}, {param_c}, {param_h}, {param_d}, {param_hh}, {param_dd}, {param_hd}]\n')
        # output.write(f'ev.r.d.: {evrd}\n')
        # #output.write(decays_line)
        # #output.write(rates_line)
        # output.write(lc.cycle_to_str([pretty_frame], TORUS_SIZE, True) + '\n')

order_filename = f'FinalOrderT{TORUS_SIZE}x{TORUS_SIZE}.txt'
with open(order_filename) as order_input:
    ordering = [ int(id.strip()) for id in order_input.readlines()]

    output.write(f'#{id}: [{period}, {param_c}, {param_h}, {param_d}, {param_hh}, {param_dd}, {param_hd}]\n')
    output.write(f'ev.r.d.: {evrd}\n')
    output.write(decays_line)
    output.write(rates_line)
    output.write(lc.cycle_to_str([pretty_frame], TORUS_SIZE, True) + '\n')