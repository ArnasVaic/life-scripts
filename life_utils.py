import life_io as lio
import numpy as np

def count_alive_pairs_along_axis_edge(frame, axis):
    # cell values at opposing edges
    opposing = np.take(frame, [0, -1], axis=axis)
    # summing alive pairs will yield value of 2
    sum = np.sum(opposing, axis=axis)
    # count number of twos
    return np.sum(sum == 2)

def count_alive_diag_pairs_along_axis_edge(frame, axis):
    # cell values at opposing edges
    edges = np.take(frame, [0, -1], axis=axis)
    
    # take one of the edges. It doesn't really matter which
    last = edges[1, :] if axis == 0 else edges[:, 1] 

    # last is always going to be 1d
    # make copies where its shifted right and left
    last_left = np.roll(last, shift=-1)
    last_right = np.roll(last, shift=1)
    
    # replace line with left shifted
    if axis == 0:
        # edges shape is [2, n]
        edges[1, :] = last_left
    if axis == 1:
        # edges shape is [n, 2]
        edges[:, 1] = last_left

    s1 = np.sum(np.sum(edges, axis=axis) == 2)

    # replace line with right shifted
    if axis == 0:
        # edges shape is [2, n]
        edges[1, :] = last_right
    if axis == 1:
        # edges shape is [n, 2]
        edges[:, 1] = last_right

    s2 = np.sum(np.sum(edges, axis=axis) == 2)

    return s1 + s2

def find_pretty(frame, debug=False):
  sy = find_pretty_offset_for_axis(frame, 0, debug)
  sx = find_pretty_offset_for_axis(frame, 1, debug)
  return np.roll(frame, shift=(sx, sy), axis=(1, 0))

def calculate_penalty(frame, axis):
    alpha, beta = 3, 1
    p = count_alive_pairs_along_axis_edge(frame, axis)
    q = count_alive_diag_pairs_along_axis_edge(frame, axis)
    return alpha * p + beta * q

def find_pretty_offset_for_axis(frame, axis, debug=False):

    # if has exactly one empty column, place on it
    zero_lines = np.all(frame == 0, axis=1-axis)

    if np.sum(zero_lines) == 1:
        
        zero_line_id = np.argwhere(np.all(frame == 0, axis=1-axis)==True)[0][0]

        if debug:
            print(f'[axis={axis}] Single empty line at {zero_line_id}.')

        return -zero_line_id

    if debug:
        print(f'[axis={axis}] No single empty line.')

    # start by initializing the minimum penalty
    min_penalty = calculate_penalty(frame, axis)
    pretty_frame = frame
    best_offset = 0

    if debug:
        print(f'[axis={axis}] Initial penatly is {min_penalty}.')

    # go through each possible offset
    for offset in range(frame.shape[axis]):

        shifted_frame = np.roll(frame, shift=offset, axis=axis)

        penalty = calculate_penalty(shifted_frame, axis)

        if min_penalty > penalty:

            if debug:
                print(f'[axis={axis}] Better penatly found {penalty} at offset {offset}.')

            min_penalty = penalty
            best_offset = offset
            pretty_frame = shifted_frame

        # if the penalty is 0 that means we can stop early
        # and just try to center the frame on a given axis.
        if penalty == 0:
            break

    if penalty != 0:

        if debug:
            print(f'[axis={axis}] Not possible to center.')

        # we can't do better for now
        return best_offset
    
    if debug:
        print(f'uncentered frame:')
        lio.show(pretty_frame)

    # indices of cells that are not zero
    indices = np.argwhere(pretty_frame != 0)

    start, end = np.min(indices[:, axis]), np.max(indices[:, axis])
    length = end - start + 1

    # given axis coordinate of bounding box if the bounding box
    # was centered on this axis. 
    centered_start = (frame.shape[axis] - length) / 2
    center_offset = int(centered_start - start)

    if debug:
        print(f'[axis={axis}] Possible to center, start={start}, end={end}, length={length}, offset to center={best_offset + center_offset}.')

    return best_offset + center_offset
