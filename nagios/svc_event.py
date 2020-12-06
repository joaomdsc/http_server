# svc_event.py - servcie event handler

"""Arguments are $SERVICESTATE$ $SERVICESTATETYPE$ $SERVICEATTEMPT$"""

import os
import sys
from datetime import datetime

# Command line arguments
if len(sys.argv) != 4:
    print(f'Usage: {sys.argv[0]} <service state> <state type> <attempt>')
    sys.exit(3)

state = sys.argv[1]
type = sys.argv[2]
attempt = sys.argv[3]

# Log
n = datetime.now()
dt = n.strftime("%Y-%m-%d %H:%M:%S")
ts = int(n.timestamp())

# nagios user does not have the HOME environment variable set
logpath = '/tmp/events.log'
with open(logpath, 'a') as f:
    f.write(f'{dt}: {ts}: svc_event: {state} {type} {attempt}\n')
