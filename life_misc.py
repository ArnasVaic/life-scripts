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