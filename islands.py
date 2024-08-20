# %%

import life_io as lio
import life_core as lc
import life_misc as lm
import life_utils as lu
import numpy as np
import re

for torus_size in range(6, 7):

    input_filename = f'Torus{torus_size}x{torus_size}.txt'
    output_filename = f'Islands{torus_size}x{torus_size}.txt'

    # for every cycle in the file this array should have non None values
    # only for cycles that have a single island. The values should also
    # be not entire frame but cutouts of the island (smallest size that fits the island)
    # at the index positions of which frames do not have a single island should be 
    # None values that would ensure correct indexing of the further cutouts
    all_cutouts = []

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

            # find the cycle and make each frame pretty
            cycle = lc.find_cycle(frame)
            pretty_cycle = [ lu.find_pretty(f) for f in cycle ]

            cycle_island_coords = [ lm.get_island_coords(f) for f in pretty_cycle]

            frame_island_count = [ len(coords) for coords in cycle_island_coords ]
            frame_id = np.argmin(frame_island_count)           

            # get bounding boxes for each frame
            cycle_bounding_boxes = [ [ lm.island_bounding_box(frame, *coord) for coord in frame_island_coords] for frame_island_coords, frame in zip(cycle_island_coords, pretty_cycle) ]
            
            # theoretically equal to cycle_bounding_boxes[0]
            #bounding_boxes = [ lm.island_bounding_box(pretty_cycle[frame_id], *coord) for coord in cycle_island_coords[frame_id] ]

            # when frame contains only a single island that cycle becomes the owner
            # of said island and its id will be reffered to later if this island comes 
            # up in other configurations where it is not alone.
            for bounding_boxes in cycle_bounding_boxes:
                cycle_cutouts = []
                if len(bounding_boxes) == 1:
                    # add c
                    # single island
                    box = bounding_boxes[0]
                    cutout = pretty_cycle[frame_id][box[0]:box[1]+1, box[2]:box[3]+1]
                    cycle_cutouts.append(cutout)
                all_cutouts.append(cycle_cutouts)

            id = int(re.search(r'#(\d+)', config_line).group(1))
            if id != 2:
                continue

            print(f"#{id:}")
            #print( lc.cycle_to_str(pretty_cycle, torus_size, True) )
            #print([ lm.island_cells(pretty_cycle[frame_id], *coord) for coord in cycle_island_coords[frame_id] ][0])
            print(cycle_island_coords[frame_id])
            island_ids = []
            for box in bounding_boxes:
                
                box_width = box[1] - box[0] + 1
                box_height = box[3] - box[2] + 1

                #print(box)
                # smaller frame that contains only the current island
                cutout = pretty_cycle[frame_id][box[0]:box[1]+1, box[2]:box[3]+1]

                # # cutout pasted on empty frame
                # padded = np.pad(cutout, [(0, torus_size - box_width), (0, torus_size - box_height)], mode='constant', constant_values=0)

                # find pretty can be moved to else branch
                # placed here only for printing purposes
                # padded_pretty = lu.find_pretty(padded)
                # print(lc.display(padded_pretty))

                cutout_cell_count = np.count_nonzero(cutout)

                if cutout_cell_count < 3:
                    # no islands can survive with less than 3 cells
                    # formal requirement: for islands that dont have an id
                    # show the island cell count with a negative sign.
                    island_ids.append(-cutout_cell_count)
                else:
                    island_id = lu.find_cycle_id(cutout, all_cutouts)
                    island_ids.append(island_id if island_id != None else -cutout_cell_count)

            print(island_ids)

            
            


# %%

import life_utils as lu

raw_frame = """
- - - - - - 
- - - - - - 
- - O O - - 
- O - - O - 
- - O O - - 
- - - - - - """

f = lio.parse_pretty_frame(raw_frame, 8, 'O', '-', ' ')

p1 = lu.find_pretty(f)
p2 = lu.find_pretty(p1)
print(lc.display(p1))
print(lc.display(p2))
# %%
