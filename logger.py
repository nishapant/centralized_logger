import socket
import sys
 
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = int(sys.argv[1])
 
server_address = ('localhost', port)
tcp_socket.bind(server_address)
 
tcp_socket.listen(1)
 
while True:
    print("Waiting for connection")
    connection, client = tcp_socket.accept()

    print(client)
 
    try:
        print("Connected to client IP: {}".format(client))
         
        while True:
            data = connection.recv(1000).decode("utf-8")

            parts = data.split('\n')
            
            if parts[0] == "c" and len(parts) > 2:
                print(parts[1] + " - " + parts[2] + " connected")
            else:
                print(data[:-1])

 
            if not data:
                break
 
    except Exception:
        connection.close()