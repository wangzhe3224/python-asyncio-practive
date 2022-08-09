import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
address = ("127.0.0.1", 8000)
server_socket.bind(address)
server_socket.listen()

try:
    
    conn, client_addr = server_socket.accept()
    print(f"I got a connection from {client_addr}")

    buffer = b''
    
    while buffer[-2: ] != b'\r\n':
        data = conn.recv(2)
        if not data:
            break
        else:
            print(f"I got data: {data}!")
            buffer += data
        
    print(f"all data I got: {buffer}")
    print(f"echo back to client")
    conn.sendall(buffer)

except:
    server_socket.close()