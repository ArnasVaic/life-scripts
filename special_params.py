def calculate_param_h(state, torus_size, step=1):
    sum = 0
    for i in range(torus_size):
        for j in range(torus_size):
            if state[i, j] == 1:
                if state[i, (j + step) % torus_size] == 1:
                    sum = sum + 1
                if state[(i + step) % torus_size, j] == 1:
                    sum = sum + 1
    return sum

def calculate_param_d(state, torus_size, step=1):
    sum = 0
    for i in range(torus_size):
        for j in range(torus_size):
            if state[i, j] == 1:
                next_i, next_j, prev_i = (i + step) % torus_size, (j + step) % torus_size, (i + torus_size - step) % torus_size
                if state[next_i, next_j] == 1:
                    sum = sum + 1
                if state[prev_i, next_j] == 1:
                    sum = sum + 1
    return sum

def calculate_param_hd(state, torus_size):
    # - 4 - -
    # - - 3 -
    # O - - -
    # - - 1 -
    # - 2 - -
    s1, s2, s3, s4 = 0, 0, 0, 0
    for i in range(torus_size):
        for j in range(torus_size):
            if state[i, j] == 1:
                if state[(i + 1) % torus_size, (j + 2) % torus_size] == 1:
                    s1 = s1 + 1
                if state[(i + 2) % torus_size, (j + 1) % torus_size] == 1:
                    s2 = s2 + 1
                if state[(i + torus_size - 1) % torus_size, (j + torus_size + 2) % torus_size] == 1:
                    s3 = s3 + 1
                if state[(i + torus_size - 2) % torus_size, (j + torus_size + 1) % torus_size] == 1:
                    s4 = s4 + 1
    #print(s1, s2, s3, s4)
    return s1 + s2 + s3 + s4