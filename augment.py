# %%

from cycle import read_pretty_cycle_data
from scipy.signal import convolve2d
from prettify import find_pretty
import numpy as np
import re
import special_params as sp
import life_core as lc
from utils import pretty_fraction

TORUS_SIZE = 7
input_filename = f'Torus{TORUS_SIZE}x{TORUS_SIZE}.txt'
output_filename = f'Torus{TORUS_SIZE}x{TORUS_SIZE}-augmented.txt'
eigenvalue_filename = f'EigenValues{TORUS_SIZE}x{TORUS_SIZE}.txt'

with open(input_filename) as input, \
    open(eigenvalue_filename) as eigenvalue_input, \
    open(output_filename, 'w') as output:
    
    toruses_read = 0

    while True:

        print(f'Number of toruses read: {toruses_read}')
        toruses_read = toruses_read + 1

        # read the configuration (4 + N lines per configuration)
        config_line, decays_line, rates_line = input.readline(), input.readline(), input.readline()

        if not config_line:
            break

        frame = read_pretty_cycle_data(input, TORUS_SIZE, 'O', '-', ' ')
        empty_line = input.readline()
        pretty_frame = find_pretty(frame, TORUS_SIZE)

        cycle = [frame]

        current = frame
        while True:
            current = lc.life_next(current, TORUS_SIZE)
            if np.array_equal(current, cycle[0]):
                break
            cycle.append(current)


        # new eigen value
        eigenvalue = eigenvalue_input.readline().strip()

        # parse config line
        id = int(re.search(r'#(\d+)', config_line).group(1))
        period = int(re.search(r'c(\d+)', config_line).group(1))
        
        param_c = pretty_fraction(sum([f.sum() for f in cycle]), period)
        param_h = pretty_fraction(sum([sp.calculate_param_h(f, TORUS_SIZE) for f in cycle]), period)
        param_d = pretty_fraction(sum([sp.calculate_param_d(f, TORUS_SIZE) for f in cycle]), period)

        param_hh = pretty_fraction(sum([sp.calculate_param_h(f, TORUS_SIZE, 2) for f in cycle]), period)
        param_dd = pretty_fraction(sum([sp.calculate_param_d(f, TORUS_SIZE, 2) for f in cycle]), period)
        param_hd = pretty_fraction(sum([sp.calculate_param_hd(f, TORUS_SIZE) for f in cycle]), period)

        # output new config line
        output.write(f'#{id}: p={period}: c={param_c}: h={param_h}: d={param_d}: hh={param_hh}: dd={param_dd}: hd={param_hd}:\n')
        output.write(f'ev: {eigenvalue}\n')
        output.write(decays_line)
        output.write(rates_line)
        output.write(lc.cycle_to_str([pretty_frame], TORUS_SIZE, True) + '\n')

# %%
