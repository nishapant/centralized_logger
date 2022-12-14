import socket
import sys
import time

node_name = sys.argv[1]
ip_addr = sys.argv[2]
port = int(sys.argv[3])

# Create a connection to the server application on port 81
tcp_socket = socket.create_connection((ip_addr, port))

# Format for all data: [<time> <nodename> <[c\n OR hash]>]
data = str(time.time()) + "\n" + node_name + "\nc\n"
data_bytes = bytes(data, 'utf-8')
tcp_socket.send(data_bytes)

time.sleep(2)

try:
    for line in sys.stdin:
        parts = line.split(' ')
        print("node:", parts)
        data = bytes(parts[0] + "\n" + node_name + "\n" + parts[1], 'utf-8')
        tcp_socket.send(data)

finally:
    print("Closing socket")
    tcp_socket.close()