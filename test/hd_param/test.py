# %%
import life_core as lc
from cycle import read_pretty_cycle_data
import special_params as sp 

with open('test/hd_param/input.txt') as input:
    frame = read_pretty_cycle_data(input, 7, 'O', '-', ' ')

    print(frame)
    print(sp.calculate_param_d(frame, 7, 2))

    print(lc.life_next(frame, 7))
    print(sp.calculate_param_d(lc.life_next(frame, 7), 7, 2))
# %%
