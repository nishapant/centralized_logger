import socket
import sys
import time
from threading import Thread, Lock

# Statics 
MAX_NODES = 8 # as specified in documentation

# Data
node_metadata = {} 
node_data = {}

def run_server(server_port):
    # Run 
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_address = ('localhost', server_port)
    tcp_socket.bind(server_address)
    
    tcp_socket.listen(MAX_NODES)
    
    while True:
        print("Waiting for connection...")
        connection, client = tcp_socket.accept()

        node_ip = client[0]
        node_port = client[1]
    
        t = Thread(target=connect_node, args=(connection, node_ip, node_port,))
        t.start()

def connect_node(connection, node_ip, node_port):
    try:
        # print("Connected to client IP: {}".format(client))
        while True:
            data = connection.recv(1000).decode("utf-8")

            parts = data.split('\n')
            start_time = parts[0]
            node_name = parts[1]
            hash_val = parts[2]

            # Print data 
            if hash_val == "c":
                print(start_time + " - " + node_name + " connected")
            else:
                print(start_time + " " + node_name + " " + hash_val)

            # Store info in dictionaries
            end_time = time.time() 
            
            if (node_name, node_ip) not in node_metadata:
                node_metadata[(node_name, node_ip)] = node_port 
            
            data_point = (start_time, end_time, hash_val)

            if node_name not in node_data:
                node_data[node_name] = [data_point]
            else:
                node_data[node_name].append(data_point)

            # Break if error - TODO: fix this and make it disconnect 
            if not data:
                print("Disconnecting...")
                break

    except Exception:
        connection.close()

if __name__  == "__main__":
    server_port = int(sys.argv[1])
    run_server(server_port)