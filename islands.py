# %%

import life_io as lio
import life_core as lc
import life_misc as lm
import life_utils as lu
import numpy as np
import re

torus_size = 7
input_filename = f'Torus{torus_size}x{torus_size}.txt'
output_filename = f'Islands{torus_size}x{torus_size}.txt'

# for every cycle in the file this array should have non None values
# only for cycles that have a single island. The values should also
# be not entire frame but cutouts of the island (smallest size that fits the island)
# at the index positions of which frames do not have a single island should be 
# None values that would ensure correct indexing of the further cutouts
cycle_cutouts = []
with open(input_filename) as input:

    while True:
        # read the configuration (4 + N lines per configuration)
        config_line, decays_line, rates_line = input.readline(), input.readline(), input.readline()
        
        # EOF if config line was not read
        if not config_line:
            break
        
        id = int(re.search(r'#(\d+)', config_line).group(1))

        frame_lines = [input.readline() for _ in range(torus_size)]
        frame = lio.parse_pretty_frame(''.join(frame_lines), torus_size, 'O', '-', ' ')
        _ = input.readline() # empty line between frames

        # find the cycle and make each frame pretty
        cycle = lc.find_cycle(frame)
        pretty_cycle = [ lu.find_pretty(f) for f in cycle ]

        cycle_island_coords = [ lm.get_island_coords(f) for f in pretty_cycle]

        frame_island_counts = [ len(coords) for coords in cycle_island_coords ]
        
        # id of frame with least islands
        frame_id = np.argmin(frame_island_counts)
        optimal_frame = pretty_cycle[frame_id]
        optimal_frame_island_starting_coords = cycle_island_coords[frame_id]
        
        # list of set of cell coordinates for each island
        island_coord_sets = [ lm.island_cells(optimal_frame, *coord) for coord in optimal_frame_island_starting_coords ]
        
        # if there is one island register it it cutout lookup
        if frame_island_counts[frame_id] == 1:
            island_cell_coords = island_coord_sets[0]    
            cutout = lm.get_pretty_island_cutout(optimal_frame, island_cell_coords)
            cycle_cutouts.append(cutout)
        else:
            cycle_cutouts.append(None)



with open(input_filename) as input, open(output_filename, 'w') as output:
    
    while True:

        # read the configuration (4 + N lines per configuration)
        config_line, decays_line, rates_line = input.readline(), input.readline(), input.readline()
        
        # EOF if config line was not read
        if not config_line:
            break
        
        id = int(re.search(r'#(\d+)', config_line).group(1))

        frame_lines = [input.readline() for _ in range(torus_size)]
        frame = lio.parse_pretty_frame(''.join(frame_lines), torus_size, 'O', '-', ' ')
        _ = input.readline() # empty line between frames

        # find the cycle and make each frame pretty
        cycle = lc.find_cycle(frame)
        pretty_cycle = [ lu.find_pretty(f) for f in cycle ]

        cycle_island_coords = [ lm.get_island_coords(f) for f in pretty_cycle ]
        frame_island_count = [ len(coords) for coords in cycle_island_coords ]
        frame_id = np.argmin(frame_island_count)           
        optimal_frame = pretty_cycle[frame_id]
        optimal_frame_island_starting_coords = cycle_island_coords[frame_id]
        # if id == 26:
        #     print(f"frame with least islands: {frame_id}")
        #     print(lc.cycle_to_str(pretty_cycle, torus_size, True))

        # get bounding boxes for each frame
        #cycle_bounding_boxes = [ [ lm.island_bounding_box(frame, *coord) for coord in frame_island_coords] for frame_island_coords, frame in zip(cycle_island_coords, pretty_cycle) ]
        
        # theoretically equal to cycle_bounding_boxes[0]
        island_coord_sets = [ lm.island_cells(optimal_frame, *coord) for coord in optimal_frame_island_starting_coords ]
        #bounding_boxes = [ lm.island_bounding_box(pretty_cycle[frame_id], *coord) for coord in cycle_island_coords[frame_id] ]

        # when frame contains only a single island that cycle becomes the owner
        # of said island and its id will be reffered to later if this island comes 
        # up in other configurations where it is not alone.
        #for bounding_boxes in cycle_bounding_boxes:
            
        # if len(bounding_boxes) == 1:
        #     # single island
        #     box = bounding_boxes[0]

        #     # this is pretty daring, generaly I don't know if there existis a configuration 
        #     # concave enough so that the bounding box would contain other island.
        #     cutout = pretty_cycle[frame_id][box[0]:box[1]+1, box[2]:box[3]+1]

        #     cycle_cutouts.append(cutout)
        # else:
        #     cycle_cutouts.append(None)

        # if id != 26:
        #     continue

        #print( lc.cycle_to_str(pretty_cycle, torus_size, True) )
        #print([ lm.island_cells(pretty_cycle[frame_id], *coord) for coord in cycle_island_coords[frame_id] ][0])
        #print(cycle_island_coords[frame_id])
        
        island_ids = []
        for cell_coords in island_coord_sets:
            
            cutout = lm.get_pretty_island_cutout(optimal_frame, cell_coords)
            cutout_cell_count = np.count_nonzero(cutout)

            if cutout_cell_count < 3:
                # no islands can survive with less than 3 cells
                # formal requirement: for islands that dont have an id
                # show the island cell count with a negative sign.
                island_ids.append(-cutout_cell_count)
            else:
                island_id = lu.find_cycle_id(cutout, cycle_cutouts)
                island_ids.append(island_id if island_id != None else -cutout_cell_count)

        #print(f"#{id}, {island_ids}")
        
        # process island ids
    
        nonnegative_ids = [ x for x in island_ids if x >= 0 ]
        nonnegative_ids.sort()
        negative_ids = [ x for x in island_ids if x < 0 ]
        negative_ids.sort()
        island_ids = nonnegative_ids + negative_ids
        output.write(f'{island_ids}\n')
        # for island_id in island_ids:
        #     if island_id >= 0:
        #         #print(lc.display(cycle_cutouts[island_id - 1]))
        #     else:
                #print("island cutout does not exist.")

    # for cycle_cutouts in all_cutouts:
    #     for cutout in cycle_cutouts:
    #         print(lc.display(cutout))
    #     print('---')

        
        


# %%

import life_io as lio
import life_utils as lu
import life_misc as lm

raw_frame = """
- - - - - - - -   
- - - - - - - -   
- O - - O - O O   
O O O O O - O -   
- - - - - - - -   
- O O O O O O O   
- O - - O - - O   
- - - - - - - - """

f = lio.parse_pretty_frame(raw_frame, 8, 'O', '-', ' ')
lio.show(f)
print(lm.get_island_coords(f))
# %%
