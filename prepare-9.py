# Rough plan for preparing 9x9 files:
# - Special parameter file
# - Island id file
# - Eigen file with
# Read the config id and parse/make the cycle
# %%
import numpy as np
import life_utils as lu
import life_core as lc
import life_misc as lm
import life_io as lio
from utils import pretty_fraction

TORUS_SIZE = 9
cycle_frame_ids_filename = f'OrderedCycleFrameIds{TORUS_SIZE}x{TORUS_SIZE}.txt'
decay_rates_filename = f'FinalMatrixT{TORUS_SIZE}x{TORUS_SIZE}.txt'
evrd_filename = f'EvRelativeDiffsT{TORUS_SIZE}x{TORUS_SIZE}.txt'
output_filename = f'Torus{TORUS_SIZE}x{TORUS_SIZE}-v1-long.txt'
special_params_filename = f'SpecialParams{TORUS_SIZE}x{TORUS_SIZE}.txt'

def parse_pretty_cycle( line ):
    str_id = line.strip()
    id = int(str_id)
    bin_id = bin(id)[2:].zfill(TORUS_SIZE ** 2)
    array = np.array([ int(digit) for digit in bin_id ])
    reshaped = np.reshape(array, (TORUS_SIZE, TORUS_SIZE))
    cycle = lc.find_cycle(reshaped)
    return [ lu.find_pretty(f) for f in cycle ]

def parse_decay_rates( line ):
    decays_span_indices = (1, line.index(']'))
    rates_span_indices = (line.rindex('[') + 1, line.rindex(']')) 
    factor_span_start = line.rindex(',') + 1
    
    decays_span = line[decays_span_indices[0]:decays_span_indices[1]]
    rates_span = line[rates_span_indices[0]:rates_span_indices[1]]
    factor_span = line[factor_span_start:]
    
    decays = [ int(token) for token in decays_span.split(',') ]
    rates = [ int(token) for token in rates_span.split(',') ]
    factor = int(factor_span)
    
    return decays, rates, factor
    
def parse_evrd(line):
    return line.strip()

def special_params_array(cycle):
    p = len(cycle)
    c = pretty_fraction(sum([f.sum() for f in cycle]), p)
    h = pretty_fraction(sum([lm.calculate_param_h(f) for f in cycle]), p)
    d = pretty_fraction(sum([lm.calculate_param_d(f) for f in cycle]), p)
    hh = pretty_fraction(sum([lm.calculate_param_h(f, 2) for f in cycle]), p)
    dd = pretty_fraction(sum([lm.calculate_param_d(f, 2) for f in cycle]), p)
    hd = pretty_fraction(sum([lm.calculate_param_hd(f) for f in cycle]), p)
    return [ f'{p}', c, h, d, hh, dd, hd ]
    # return f'p={p}: c={c}: h={h}: d={d}: hh={hh}: dd={dd}: hd={hd}'

with open(cycle_frame_ids_filename) as cycle_frame_ids_file, \
    open(decay_rates_filename) as decay_rates_file, \
    open(evrd_filename) as ev_relative_diffs_file, \
    open(output_filename, 'w') as output_file, \
    open(special_params_filename, 'w') as special_params_file:
    
    cycles_read = 0
    
    while True:
        
        cycle_frame_id_line = cycle_frame_ids_file.readline()
        decay_rates_line = decay_rates_file.readline()
        evrd_line = ev_relative_diffs_file.readline()

        if not cycle_frame_id_line:
            print(f"Process complete, cycles_read: {cycles_read}")
            break
        
        
        pretty_cycle = parse_pretty_cycle(cycle_frame_id_line)
        special_params = special_params_array(pretty_cycle)
        
        special_params_file.write(f'[{ ','.join(special_params) }]\n')
        
        # decays, rates, factor = parse_decay_rates(decay_rates_line)
        # evrd = parse_evrd(evrd_line)
    
        # output_file.write(f'#{cycles_read + 1}: {special_params}\n')
        # output_file.write(f'ev.r.d.: {evrd}\n')
        # output_file.write(f'decays: {','.join([f'{d}' for d in decays])}\n')
        # output_file.write(f'rates: {','.join([ pretty_fraction(rate, factor) for rate in rates ])}\n')
        # output_file.write(f'{lc.display(pretty_cycle[0])}\n')
        
        cycles_read = cycles_read + 1
    
     
# %%
