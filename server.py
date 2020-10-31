# server.py - writing an HTTP server from scratch
# Based on https://bhch.github.io/posts/2017/11/writing-an-http-server-from-scratch/

# Firefox: User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0
# Chrome : User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36

import sys
import socket
      
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
# TCPServer
#-------------------------------------------------------------------------------

class TCPServer:
    def __init__(self, host='127.0.0.1', port=80):
        self.host = host
        self.port = port
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print(f'Listening at {s.getsockname()}')

        while True:
            try:
                conn, addr = s.accept()
            except KeyboardInterrupt:
                print('\nCtrl-C, exiting.')
                sys.exit()
            print(f'Connected by {addr}')
            
            # Read the first 1024 bytes of data from the client
            data = conn.recv(1024)
            print(data.decode())

            # Prepare the response
            resp = self.handle_request(data)
            
            # Echo the data back to the client. 
            conn.sendall(resp)
            conn.close()
    
#-------------------------------------------------------------------------------
# HTTPServer
#-------------------------------------------------------------------------------

class HTTPServer(TCPServer):
    def handle_request(self, data):
        # Chrome says ERR_INVALID_HTTP_RESPONSE if the first line is omitted.
        return b'HTTP/1.1 200 OK\n\n' + data
    
#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

srv = HTTPServer()
