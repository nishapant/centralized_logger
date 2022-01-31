import socket
import sys
import time
import signal
import os

from threading import Thread, Lock

# Statics 
MAX_NODES = 8 # as specified in documentation

# Data
node_metadata = {} 
node_data = {}
thread_list = []
shutdown = False

def run_server(server_port):
    # Run 
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)

    server_address = (local_ip, server_port)
    tcp_socket.bind(server_address)
    
    tcp_socket.listen(MAX_NODES)

    print("Nodes can now be connected...")

    while True:
        connection, client = tcp_socket.accept()

        node_ip = client[0]
        node_port = client[1]
    
        t = Thread(target=connect_node, args=(connection, node_ip, node_port,))
        thread_list.append(t)
        t.start()

def connect_node(connection, node_ip, node_port):
    node_name = ""

    try:
        # print("Connected to client IP: {}".format(client))
        while True and shutdown == False:
            while shutdown != True:
                data = connection.recv(1000).decode("utf-8")
                break 

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
            end_time = str(time.time())
            
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
        curr_time = str(time.time())
        print(curr_time + " - " + node_name + " disconnected")
        print(node_metadata)
        print(node_data)

        connection.close()



### THIS IS JUST FOR EXIT HANDLING so the error doesnt appear and we can terminate the threads

def handler(signum, frame):
    print("Join threads...")
    shutdown = True
    print(thread_list)
    for thread in thread_list:
        thread.join()

    print("Server shutdown...")
    exit(0)

signal.signal(signal.SIGINT, handler)


if __name__  == "__main__":
    server_port = int(sys.argv[1])
    run_server(server_port)