# %%

import life_io as lio
import life_core as lc
import life_misc as lm
from utils import pretty_fraction
import numpy as np
import re

for torus_size in range(6, 10):

    input_filename = f'Torus{torus_size}x{torus_size}.txt'
    output_filename = f'SpecialParams{torus_size}x{torus_size}.txt'

    with open(input_filename) as input, open(output_filename, 'w') as output:
        
        while True:

            # read the configuration (4 + N lines per configuration)
            config_line, decays_line, rates_line = input.readline(), input.readline(), input.readline()

            # EOF if config line was not read
            if not config_line:
                break

            frame_lines = [input.readline() for _ in range(torus_size)]
            frame = lio.parse_pretty_frame(''.join(frame_lines), torus_size, 'O', '-', ' ')
            _ = input.readline() # empty line between frames

            cycle = [frame]

            current = frame
            while True:
                current = lc.life_next(current, torus_size)
                if np.array_equal(current, cycle[0]):
                    break
                cycle.append(current)
            
            period = int(re.search(r'c(\d+)', config_line).group(1))
        
            param_c = pretty_fraction(sum([f.sum() for f in cycle]), period)
            param_h = pretty_fraction(sum([lm.calculate_param_h(f) for f in cycle]), period)
            param_d = pretty_fraction(sum([lm.calculate_param_d(f) for f in cycle]), period)

            param_hh = pretty_fraction(sum([lm.calculate_param_h(f, 2) for f in cycle]), period)
            param_dd = pretty_fraction(sum([lm.calculate_param_d(f, 2) for f in cycle]), period)
            param_hd = pretty_fraction(sum([lm.calculate_param_hd(f) for f in cycle]), period)

            # output new config line
            output.write(f'[{period}, {param_c}, {param_h}, {param_d}, {param_hh}, {param_dd}, {param_hd}]\n')
# %%
