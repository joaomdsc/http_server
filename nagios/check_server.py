# check_server.py - generic simulated server check

import os
import sys
import json
from datetime import datetime

min = 0
max = 1
warn = 0.6
crit = 0.8

# Command line args
hostname = sys.argv[1]
hoststate = sys.argv[2]

# Determine value from file
filepath = os.path.join(os.getenv('HOME'), 'status_server.json')
val = 0.5
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        obj = json.load(f)
    if hostname in obj:
        val = obj[hostname]
except FileNotFoundError:
    pass

state = (0, 'OK') if val < warn \
  else (1, 'Warning') if val < crit \
  else (2, 'Critical')
  
first_line = f'{state[1]}: val={val} | val={val};{warn};{crit};{min}; [{hostname}:{hoststate}]'
print(first_line)

# Log to /var/lib/centreon-engine
dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logpath = os.path.join(os.getenv('HOME'), 'check_server.log')
with open(logpath, 'a') as f:
    f.write(f'{dt}: {first_line}\n')

sys.exit(state[0])
