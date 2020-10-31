# server.py - writing an HTTP server from scratch
# Based on https://bhch.github.io/posts/2017/11/writing-an-http-server-from-scratch/

# Firefox: User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0
# Chrome : User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36

import os
import sys
import socket
import mimetypes
      
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
    blank = b'\n'

    headers = {
        'Server': 'Joao Server',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found.',
        501: 'Not Implemented.',
    }

    def resp_line(self, code):
        """Return the response line (as binary)."""
        reason = self.status_codes[code]
        line = f'HTTP/1.1 {code} {reason}\n'
        return line.encode()

    def resp_headers(self, extra_headers=None):
        """Return the response headers (as binary)."""
        hdr = self.headers.copy()
        if extra_headers:
            hdr.update(extra_headers)

        # Local 'headers' variable
        headers = ''
        for h, v in hdr.items():
            headers += f'{h}: {v}\n'

        return headers.encode()

    def HTTP_501_handler(self):
        resp_line = self.resp_line(501)
        headers = self.resp_headers()
        body = b"""<html>
  <body>
    <h1>501 Not Implemented</h1>
  </body>
</html>
"""
        return resp_line + headers + self.blank + body

    def handle_GET(self, req):
        filename = req.uri.strip('/')

        if os.path.exists(filename):
            resp_line = self.resp_line(200)
            content_type = mimetypes.guess_type(filename)[0] or 'text/html'
            extra_headers = {'Content-Type': content_type}
            headers = self.resp_headers(extra_headers)
            with open(filename, 'rb') as f:
                body = f.read()
        else:
            resp_line = self.resp_line(404)
            headers = self.resp_headers()
            body = b"""<html>
  <body>
    <h1>404 Not Found</h1>
  </body>
</html>
"""
        return resp_line + headers + self.blank + body            
        
    def handle_request(self, data):
        req = HTTPRequest(data)
        try:
            handler = getattr(self, f'handle_{req.method}')
        except AttributeError:
            handler = self.HTTP_501_handler
        return handler(req)
    
#-------------------------------------------------------------------------------
# HTTPRequest
#-------------------------------------------------------------------------------

class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.version = '1.1'

        lines = data.split(b'\n')
        request = lines[0]
        words = request.split()

        self.method = words[0].decode()

        if len(words) > 1:
            # Sometimes browsers woon't send uri for homepage
            self.uri = words[1].decode()

        if len(words) > 2:
            self.version = words[2].decode()
        
    
#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

srv = HTTPServer()
