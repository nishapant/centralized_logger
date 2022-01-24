import socket
import sys
import time
# node_name = sys.argv[0] if sys.argv[0] else "node1"
# ip_addr = sys.argv[1] if sys.argv[1] else "localhost"
# port = int(sys.argv[2]) if sys.argv[2] else 8080

node_name = sys.argv[1]
ip_addr = sys.argv[2]
port = int(sys.argv[3])

# Create a connection to the server application on port 81
tcp_socket = socket.create_connection((ip_addr, port))

# Format for all data: [<time> <nodename> <[c\n OR hash]>]
data = bytes(str(time.time()) + "\n" + node_name + "\nc", 'utf-8')
tcp_socket.send(data)
 
try:
    for line in sys.stdin:
        print(line)
        parts = line.split(' ')
        data = bytes(parts[0] + "\n" + node_name + "\n" + parts[1], 'utf-8')
        tcp_socket.send(data)
 
finally:
    print("Closing socket")
    tcp_socket.close()