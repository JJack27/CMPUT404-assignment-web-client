#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright 2019 Yizhou Zhao
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse

testing = False

def help():
    print ("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port=80):
        # use sockets!
        try:
            print(host, port)
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.connect((host, port))
            if testing:
                print("Connected to:", host,port)
        except Exception as e:
            print(e)
        return client_sock

    def get_code(self, data):
        code = int(data.split(" ")[1])
        return code

    def get_headers(self,data):
        header = data.split('\r\n\r\n')[0]
        return header

    def get_body(self, data):
        body = data.split('\r\n\r\n')[1]
        return body[:]

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')
    
    
    def parse_url(self, url):
        host = ""
        port = 80
        path = ""
        parse_result = urlparse(url)
        
        # get host and port number
        if(':' not in parse_result.netloc):
            host = parse_result.netloc
        else:
            host, port = parse_result.netloc.split(':')

        # modifying path if it's empty
        if(parse_result.path == ""):
            path = "/"
        else:
            path = parse_result.path
        return (host, int(port), path)
            

    def GET(self, url, args=None):
        code = 500
        body = ""
        response = ""
        request = ""
        client_sock = None 

        # parse url and connect to the server
        host, port, location = self.parse_url(url)
        client_sock = self.connect(host, port)
        
        # build HTTP request
        request = "GET {LOCATION} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n".format(LOCATION=location, HOST=host, PORT=port)
        
        if (args != None):
            for key in args:
                request += "{KEY}: {VALUE}\r\n".format(key, args[key])
        request += "\r\n"
        if testing:
            print("===== request =====")
            print(request)
            print("===================")

        # send HTTP request
        '''
        try:
            
            if testing:
                print("data sent")
            response = self.recvall(client_sock)
        except Exception as e:
            code = 404
            body = ""
            print(e)
            client_sock.close()
            return HTTPResponse(code, body)
        '''
        client_sock.sendall(request.encode())
        client_sock.shutdown(socket.SHUT_WR)
        if testing:
            print("data sent")
        response = self.recvall(client_sock)

        if testing:
            print("========= Response =========")
            print(response)
            print("============================")

        # parse response
        try:
            header = self.get_headers(response)
            code = int(self.get_code(header))
            body = self.get_body(response).encode("utf-8")
            if testing:
                print("code =", code)
                print("====================")
                print("header =", header)
                print("====================")
                print("body =", body)
        except Exception as e:
            print(e)
        client_sock.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = bytearray()

        # connect to the server
        


        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, args )
        else:
            return self.GET(url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print (client.command(sys.argv[2], sys.argv[1]))
    else:
        print (client.command(sys.argv[1]))
