#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos,
# Revised by Yongqin Jian 1/28/2021 for Assignment 1
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Under Apache License
# Copyright {2021} {Yongqin Jian}


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        req_method,filename = self.parse_request(self.data)

        if self.check_method(req_method):
            status = 'HTTP/1.0 200 OK\r\n'
            file_dir = self.check_file(filename)
            #print('directory:',file_dir)
            if file_dir is not None:
                # file = open('./www/base.css')
                if '.css' in file_dir or '.html' in file_dir:
                    try:
                        file = open(file_dir)
                        content = file.read()
                        file.close()

                        # 'text/html'tag provided by cor-el from: https://support.mozilla.org/en-US/questions/898460
                        if '.css' in file_dir:
                            mime = 'text/css'
                        elif '.html' in file_dir:
                            mime = 'text/html'

                        msg = status + 'content-type: '+ mime + '\r\n\r\n' + content
                        #print(msg)

                    except:
                        msg = 'HTTP/1.1 404 Not Found\r\n\r\n 404 Not Found'

                    finally:
                        self.request.sendall(bytearray(msg, 'utf-8'))

                else:
                    self.request.sendall(bytearray('HTTP/1.1 404 Not Found\r\n\r\n 404 Not Found', 'utf-8'))




        else:
            status = 'HTTP/1.1 405 Method Not Allowed\r\n'
            self.request.sendall(bytearray(status, 'utf-8'))

    @staticmethod
    def parse_request(request):
        print(request)
        request = request.decode("utf-8")
        headers = request.split('\n')
        http_method,filename,_ = headers[0].split()
        return http_method,filename

    @staticmethod
    def check_method(req_method):
        if req_method == "GET":
            return True
        else:
            print(req_method, " Not passed")
            return False

    def check_file(self, filename):
        if filename[-1] != '/' and '.' not in filename:
            filename = 'http://127.0.0.1:8080'+filename+'/'
            self.request.sendall(bytearray('HTTP/1.1 301 Moved Permanently\r\nLocation:' + filename + '\r\n', 'utf-8'))
            return None
        if filename == '/':
            filename = './www/index.html'
            return filename
        if '.' not in filename:
            filename = './www'+filename+'/index.html'
            return filename
        return './www'+filename


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
