import socket


def main():

    server_port, server_name = 12000, '127.0.0.1'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_name, server_port))
    print('The server is ready to receive...')

    try:
        while True:
            message, client_address = server_socket.recvfrom(2048)
            print(f"Client -> {client_address[0]}:{client_address[1]} -> {message.decode()}")

            modified_message = message.decode().title()
            server_socket.sendto(modified_message.encode(), client_address)
            print(f"Server -> {server_name}:{server_port} -> {modified_message}\n")
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()
        print("Server socket closed.")


if __name__ == "__main__":
    main()
