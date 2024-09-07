import numpy as np
import life_utils as lu
import life_io as lio

def calculate_param_h(frame, step=1):
    """Caclulate number of vertical and horizontal alive cell pairs that have some number of cells in between (equal to step - 1).

    Args:
        frame (_type_): Game of life configuration.
        step (int, optional): Number of steps from one cell to another. Defaults to 1.

    Returns:
        _type_: Number of pairs.
    """
    sum = 0
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            if frame[i, j] == 1:
                if frame[i, (j + step) % frame.shape[1]] == 1:
                    sum = sum + 1
                if frame[(i + step) % frame.shape[0], j] == 1:
                    sum = sum + 1
    return sum

def calculate_param_d(frame, step=1):
    """Caclulate number of diagonal alive cell pairs that have some number of cells in between (equal to step - 1).

    Args:
        frame (_type_): Game of life configuration.
        step (int, optional): Number of diagonal steps from one cell to another. Defaults to 1.

    Returns:
        _type_: Number of pairs.
    """
    sum = 0
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            if frame[i, j] == 1:
                next_i = (i + step) % frame.shape[0]
                next_j = (j + step) % frame.shape[1]
                prev_i = (i + frame.shape[0] - step) % frame.shape[0]
                if frame[next_i, next_j] == 1:
                    sum = sum + 1
                if frame[prev_i, next_j] == 1:
                    sum = sum + 1
    return sum

def calculate_param_hd(frame):
    """Caclulate number of alive cell pairs that are chess-knight move away from eachother.

    Args:
        frame (_type_): Game of life configuration.

    Returns:
        _type_: Number of pairs.
    """
    # - 4 - -
    # - - 3 -
    # O - - -
    # - - 1 -
    # - 2 - -

    s1, s2, s3, s4 = 0, 0, 0, 0
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            if frame[i, j] == 1:
                if frame[(i + 1) % frame.shape[0], (j + 2) % frame.shape[1]] == 1:
                    s1 = s1 + 1
                if frame[(i + 2) % frame.shape[0], (j + 1) % frame.shape[1]] == 1:
                    s2 = s2 + 1
                if frame[(i + frame.shape[0] - 1) % frame.shape[0], (j + frame.shape[1] + 2) % frame.shape[1]] == 1:
                    s3 = s3 + 1
                if frame[(i + frame.shape[0] - 2) % frame.shape[0], (j + frame.shape[1] + 1) % frame.shape[1]] == 1:
                    s4 = s4 + 1
    
    return s1 + s2 + s3 + s4

def dfs_mark_island(frame, x, y):
    if x < 0 or x >= frame.shape[0] or y < 0 or y >= frame.shape[1] or frame[x, y] == 0:
        return
    # Recursively erase the island
    frame[x, y] = 0
    adj_coords = [ ((x + dx + frame.shape[1]) % frame.shape[1], (y + dy + frame.shape[0]) % frame.shape[0]) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
    [dfs_mark_island(frame, *coord) for coord in adj_coords]
    
def get_island_coords(frame):
    """
    Set of coordinates (y, x) where each coordinates 
    corresponds to the the first cell that was 
    visited on that island by the algorithm.

    Args:
        frame (ndarray): numpy array representing game of life frame.

    Returns:
        set: Return set of coordinates (y, x).
    """

    frame_copy = frame.copy()
    
    island_coords = set()
    
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):

            if frame_copy[i, j] != 1:
                continue

            # We found a cell that has not been erased
            # means it's going to be a new island.
            island_coords.add((i, j))
            dfs_mark_island(frame_copy, i, j)

    return island_coords

def dfs_add_cell(frame, x, y, lookup):
    if x < 0 or x >= frame.shape[0] or y < 0 or y >= frame.shape[1] or frame[x, y] == 0 or (x, y) in lookup:
        return
    
    lookup.add((x, y))
    adj_coords = [ ((x + dx + frame.shape[1]) % frame.shape[1], (y + dy + frame.shape[0]) % frame.shape[0]) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
    [dfs_add_cell(frame, *coord, lookup) for coord in adj_coords]

def island_cells(frame, x, y):
    lookup = set()
    dfs_add_cell(frame, x, y, lookup)
    return lookup

# "pretty" is important in this case because
def get_island_pretty_cutouts(frame):
    pass

def island_bounding_box_from_coord(frame, x, y):
    cells = island_cells(frame, x, y)
    xs, ys = [ x for (x, _) in cells ], [ y for (_, y) in cells ]

    # left, right, top, bottom 
    return (min(xs), max(xs), min(ys), max(ys))

def island_bounding_box_from_cell_coords(island_cell_coords):
    xs, ys = [ x for (x, _) in island_cell_coords ], [ y for (_, y) in island_cell_coords ]

    # left, right, top, bottom 
    return (min(xs), max(xs), min(ys), max(ys))

# get pretty island cutout even if given island cell coordinates are not "continuous" e.g. wrap around edges 
def get_pretty_island_cutout(frame, uncont_island_cell_coords):
    frame_copy = frame.copy()
    for cell_y in range(frame.shape[0]):
        for cell_x in range(frame.shape[1]):
            if (cell_y, cell_x) in uncont_island_cell_coords:
                continue
            frame_copy[cell_y, cell_x] = 0
    frame_copy = lu.find_pretty(frame_copy)
    cell_coord = np.unravel_index(np.argmax(frame_copy != 0), frame_copy.shape)
    cell_coords = island_cells(frame_copy, *cell_coord)
    box = island_bounding_box_from_cell_coords(cell_coords)
    return frame_copy[box[0]:box[1]+1, box[2]:box[3]+1]