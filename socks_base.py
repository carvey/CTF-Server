import socketserver
import threading
import SimpleHTTPServer

from collections import OrderedDict
from problems import tcp_problems, udp_problems

HOST = "0.0.0.0"

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        pass

class SocketBase():

    def __init__(self):
        self.tcp_problems = OrderedDict(sorted(tcp_problems.items(), key=lambda t: t[0]))
        self.udp_problems = OrderedDict(sorted(udp_problems.items(), key=lambda t: t[0]))

        ThreadedTCPServer.allow_reuse_address = True

    def run(self):
        for problem_port, problem in self.tcp_problems.items():
            server = ThreadedTCPServer((HOST, problem_port), problem)
            ip, port = server.server_address

            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = False
            server_thread.start()

            print("%s running on port: %s" % (problem.__name__, port))

        for problem_port in self.udp_problems:
            server = socketserver.UDPServer((HOST, PORT), problem)

            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()

            print("%s running on port: %s", server_thread, port)


base = SocketBase()
base.run()
