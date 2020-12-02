# send_cmd.py - send external commands to the nagios server

from time import sleep
from datetime import datetime

def set_check_result():
    timestamp = int(datetime.now().timestamp())
    host_name = 'debian2'
    host_status = '1'  # 0=UP, 1=DOWN, 2=UNREACHABLE
    # plugin_output = "Brought it up again"
    plugin_output = "Bringing it down"

    s = f'[{timestamp}] PROCESS_HOST_CHECK_RESULT;{host_name};{host_status}' \
        + f';{plugin_output}\n'
    return s

def add_host_comment():
    timestamp = int(datetime.now().timestamp())
    host_name = 'debian2'
    persistent = 1
    author = 'Joao Moreira'
    comment = 'Comments are finally working'

    s = f'[{timestamp}] ADD_HOST_COMMENT;{host_name};{persistent};{author}' \
      + f';{comment}\n'
    return s

def send_cmd(cmd):
    cmd_file = '/usr/local/nagios/var/rw/nagios.cmd'
    print(f'Sending "{cmd.strip()}"')
    with open(cmd_file, 'w') as f:
        f.write(cmd)

# Commands
cmd = set_check_result()
# cmd = add_host_comment()

send_cmd(cmd)