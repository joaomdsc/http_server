# fake_value.py - generate a single random value

import os
import sys
from random import randrange
from datetime import datetime

min = 0
max = 1

# Command line arguments
if len(sys.argv) != 5:
    print(f'Usage: {sys.argv[0]} -w <warn> -c <crit>')
    sys.exit(3)
    
# Warning threshold
warn = float(sys.argv[2])
if warn < min or warn > max:
    print(f'warn value {warn} is not between {min} and {max}')
    sys.exit(3)
    
# Critical threshold
crit = float(sys.argv[4])
if crit < min or crit > max:
    print(f'crit value {crit} is not between min={min} and max={max}')
    sys.exit(3)
elif crit < warn:
    print(f'crit value {crit} should be greater than warn={warn}')
    sys.exit(3)

# Generate value
val = randrange(0, 100)/100

state = (0, 'OK') if val < warn \
  else (1, 'Warning') if val < crit \
  else (2, 'Critical')
  
first_line = f'{state[1]}: val={val} | val={val};{warn};{crit};{min};{max}'
print(first_line)

# Log
dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logpath = os.path.join(os.getenv('HOME'), 'fake_value.log')
with open(logpath, 'a') as f:
    f.write(f'{dt}: {first_line}\n')

sys.exit(state[0])
