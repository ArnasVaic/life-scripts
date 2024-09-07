# %%

import life_io as lio
import life_core as lc
import life_misc as lm
import life_utils as lu
import numpy as np

torus_size = 10
input_filename = f'OrderedConfigurations{torus_size}x{torus_size}.txt'
output_filename = f'Islands{torus_size}x{torus_size}.txt'

def parse_pretty_cycle( line ):
    str_id = line.strip()
    id = int(str_id)
    bin_id = bin(id)[2:].zfill(torus_size ** 2)
    array = np.array([ int(digit) for digit in bin_id ])
    reshaped = np.reshape(array, (torus_size, torus_size))
    cycle = lc.find_cycle(reshaped)
    return [ lu.find_pretty(f) for f in cycle ]

# for every cycle in the file this array should have non None values
# only for cycles that have a single island. The values should also
# be not entire frame but cutouts of the island (smallest size that fits the island)
# at the index positions of which frames do not have a single island should be 
# None values that would ensure correct indexing of the further cutouts
cycle_cutouts = []
with open(input_filename) as input:

    while True:
        # read the configuration
        line = input.readline()
        
        # EOF if config line was not read
        if not line:
            break
        
        pretty_cycle = parse_pretty_cycle(line)

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

        # read the configuration
        line = input.readline()
        
        # EOF if config line was not read
        if not line:
            break
        
        pretty_cycle = parse_pretty_cycle(line)

        cycle_island_coords = [ lm.get_island_coords(f) for f in pretty_cycle ]
        frame_island_count = [ len(coords) for coords in cycle_island_coords ]
        frame_id = np.argmin(frame_island_count)           
        optimal_frame = pretty_cycle[frame_id]
        optimal_frame_island_starting_coords = cycle_island_coords[frame_id]
        
        # theoretically equal to cycle_bounding_boxes[0]
        island_coord_sets = [ lm.island_cells(optimal_frame, *coord) for coord in optimal_frame_island_starting_coords ]
        
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
