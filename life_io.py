import numpy as np

def show(frame):
    formatted_array = np.where(frame == 0, '-', 'O')
    formatted_str = '\n'.join([' '.join(row) for row in formatted_array])
    print(formatted_str)

def parse_pretty_frame(input: str, torus_size: int, alive_symbol: str, dead_symbol: str, separator_symbol: str):
    cell_symbols = [ line.strip().split(separator_symbol) for line in input.splitlines() if line != '' ]
    cell_value_lookup = { dead_symbol: 0, alive_symbol: 1 }
    numeric_cells = [ [ cell_value_lookup[cell_symbol] for cell_symbol in line] for line in cell_symbols ]
    return np.array(numeric_cells)