import numpy as np

def read_pretty_cycle_data(file, torus_size, alive_symbol, dead_symbol, separator_symbol):

    # Numeric cell value lookup by symbol
    cell_value_lookup = { dead_symbol: 0, alive_symbol: 1 }

    # Torus is a square, so number of lines per torus will be equal to torus size
    lines = [ file.readline() for _ in range(torus_size) ]

    # 2D array filled with cell symbols
    cell_symbols = [ line.strip().split(separator_symbol) for line in lines ]
    numeric_cells = [ [ cell_value_lookup[cell_symbol] for cell_symbol in line] for line in cell_symbols ]

    return np.array(numeric_cells)