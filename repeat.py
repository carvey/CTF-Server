import socket


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('0.0.0.0', 9020)
sock.connect(server_address)

data = sock.recv(512)
string = data.split(':')[1].strip()

sock.send(string)

flags = sock.recv(512)
print(flags)
