# check_server.py - generic simulated server check

import os
import sys
from random import randrange
from datetime import datetime

min = 0
max = 1
warn = 0.6
crit = 0.8

# Generate value
# val = randrange(0, 100)/100
val = 0.5

state = (0, 'OK') if val < warn \
  else (1, 'Warning') if val < crit \
  else (2, 'Critical')
  
first_line = f'{state[1]}: val={val} | val={val};{warn};{crit};{min};{max}'
print(first_line)

# Log
dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logpath = os.path.join(os.getenv('HOME'), 'check_server.log')
with open(logpath, 'a') as f:
    f.write(f'{dt}: {first_line}\n')
    for k, v in os.environ.items():
        f.write(f'    {k}={v}\n')

sys.exit(state[0])
