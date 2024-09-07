# for large toruses there is a requirement to
# prepare output file in specific order and this
# is hard to do all at once so this script
# will prepare the torus configurations in the
# desired order.

# %%
TORUS_SIZE = 10
LINES_PER_CYCLE = 3 + TORUS_SIZE
cycles_read = 0

cycle_ids = []
with open(f'{TORUS_SIZE}x{TORUS_SIZE}-configurations-2048.txt') as input:
    while True:
        cycle_lines = [ input.readline() for _ in range(LINES_PER_CYCLE) ]
        
        if not cycle_lines[0]:
            break
        
        try: 
            id = int(cycle_lines[1].split(' ')[0])
        except ValueError:
            break
        
        cycle_ids.append(id)
        
        cycles_read = cycles_read + 1

assert len(cycle_ids) == 513875
        
orderings = []
with open(f'FinalOrderT{TORUS_SIZE}x{TORUS_SIZE}.txt') as input:
    while True:
        line = input.readline()
        
        if not line:
            break
        
        orderings.extend([ int(token) for token in line.strip().split(',') if token != ''])

assert len(orderings) == 513875

with open(f'OrderedConfigurations{TORUS_SIZE}x{TORUS_SIZE}.txt', 'w') as output:
    for i in range(len(orderings)):
        id = orderings[i]
        output.write(f'{cycle_ids[id - 1]}\n')
 # %%
