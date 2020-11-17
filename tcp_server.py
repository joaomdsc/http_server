# tcp_server.py

import sys
import socket
from _thread import start_new_thread
      
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
# on_new_client
#-------------------------------------------------------------------------------

def on_new_client(conn, port):
    cnt = 0
    while True:
        data = conn.recv(1024)
        print(f'{port}={data.decode()}')
        cnt += 1
        if cnt == 20:
            print()
            cnt = 0
        if not data: break
        data = '.'
        conn.sendall(data.encode())
    conn.close()
    
#-------------------------------------------------------------------------------
# tcp_server
#-------------------------------------------------------------------------------

def tcp_server(bind_addr, listen_port):
    # Create the socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((bind_addr, listen_port))
        s.listen(5)

        print(f'Listening at {s.getsockname()}')

        while True:
            # conn is a client socket. What's the port ?
            conn, addr = s.accept()
            print(f'tcp_server: connected from {addr}')
            start_new_thread(on_new_client, (conn, addr[1]))
    
#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

# Parse command line arguments
if len(sys.argv) not in [2, 3]:
    print(f'Usage: {sys.argv[0]} [bind_address] listen_port')
    print('Default is to bind to all available interfaces.')
    sys.exit(-1)

bind_addr = '0.0.0.0'
if len(sys.argv) == 2:
    listen_port = int(sys.argv[1])
else:
    bind_addr = sys.argv[1]
    listen_port = int(sys.argv[2])

if listen_port < 1024:
    print(f'Invalid port {listen_port}, ports below 1024 are reserved '
          'for the system.')
    sys.exit(-1)

# Create the server
tcp_server(bind_addr, listen_port)
