import socketserver
import threading
import os

from collections import OrderedDict
from http.server import SimpleHTTPRequestHandler

from problems import tcp_problems, udp_problems

HOST = "0.0.0.0"
HTTP_PORT = 8080 # need root to run on port 80

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        pass

class CTFSocketServer():

    def __init__(self):
        self.tcp_problems = OrderedDict(sorted(tcp_problems.items(), key=lambda t: t[0]))
        self.udp_problems = OrderedDict(sorted(udp_problems.items(), key=lambda t: t[0]))

        ThreadedTCPServer.allow_reuse_address = True

    def run(self):
        print("\nStarting Problems...")
        for problem_port, problem in self.tcp_problems.items():
            server = ThreadedTCPServer((HOST, problem_port), problem)
            ip, port = server.server_address

            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = False
            server_thread.start()

            print("%s started on port: %s" % (problem.__name__, port))

        for problem_port in self.udp_problems:
            server = socketserver.UDPServer((HOST, PORT), problem)

            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()

            print("%s started on port: %s", server_thread, port)

        print("\n-------\n")

    def start_http(self):
        print("\nStarting HTTP Server...")
        web_dir = os.path.join(os.path.dirname(__file__), 'web')
        os.chdir(web_dir)

        httpd = socketserver.TCPServer(("", HTTP_PORT), SimpleHTTPRequestHandler)
        httpd_thread = threading.Thread(target=httpd.serve_forever)
        httpd_thread.daemon = True
        httpd_thread.start()
        
        print("Started HTTP server on port: %s" % HTTP_PORT)

server = CTFSocketServer()
server.start_http()
server.run()

