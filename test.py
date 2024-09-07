# %%

import life_io as lio
import life_core as lc
import life_utils as lu
import numpy as np

# raw_frame = """
# O - - - - - O -   
# - - - - - O - O   
# - - - - - O O -   
# - - - O O - - -   
# - - O - O - - -   
# - O - O - - - -   
# - O O - - - - -   
# O - - - - - - O"""

raw_frame = """
- - - - - - - - - 
- - - - - - - - - 
- - - - - - - - - 
- - - - - O O - - 
- - O O - - O - - 
- - O - O O - - - 
- - - - - - - - - 
- - - - - - - - - 
- - - - - - - - - """

frame = lio.parse_pretty_frame(raw_frame, 9, 'O', '-', ' ')

print(lc.next(frame))

# %%

dy = lu.find_pretty_offset_for_axis(frame, 0, True)
dx = lu.find_pretty_offset_for_axis(frame, 1, True)

#frame = np.roll(frame, shift=dy, axis=0)
frame = np.roll(frame, shift=(-dx, dy), axis=(1, 0))

lio.show(frame)

# %%
