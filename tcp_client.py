# tcp_client.py

import sys
import socket
from time import sleep
      
#-------------------------------------------------------------------------------
# I want stdout to be unbuffered, always
#-------------------------------------------------------------------------------

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)

#-------------------------------------------------------------------------------
# tcp_client
#-------------------------------------------------------------------------------

def tcp_client(dest_addr, dest_port):
    # Create the socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f'Connecting to {dest_addr}, {dest_port}')
        s.connect((dest_addr, dest_port))
        print(f'Local port is {s.getsockname()[1]}')
        n = 0
        cnt = 0
        while True:
            msg = f'.'
            s.sendall(msg.encode())
            data = s.recv(1024)
            print(data.decode(), end='')
            cnt += 1
            if cnt == 20:
                print()
                cnt = 0
            n += 1
            sleep(1)
    
#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

# Parse command line arguments
if len(sys.argv) not in [2, 3]:
    print(f'Usage: {sys.argv[0]} [dest_address] dest_port')
    print('Default is to connect to the local host.')
    sys.exit(-1)

dest_addr = '127.0.0.1'
if len(sys.argv) == 2:
    dest_port = int(sys.argv[1])
else:
    dest_addr = sys.argv[1]
    dest_port = int(sys.argv[2])

# Create the client
tcp_client(dest_addr, dest_port)
