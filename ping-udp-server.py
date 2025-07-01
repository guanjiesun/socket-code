import socket


server_ip, server_port = '127.0.0.1', 13000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))
print('The server is ready to receive...')

try:
    while True:
        message, client_address = server_socket.recvfrom(2048)
        print(f"Client -> {client_address[0]}:{client_address[1]} -> {message.decode()}")

        ret_message = f"Pong from server: {message.decode()}" 
        server_socket.sendto(ret_message.encode(), client_address)
except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    server_socket.close()
    print("Server socket closed.")
