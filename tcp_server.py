import socket
import threading


def handle_client(conn_socket, client_addr):
    # 在 TCP 中，每一个 conn_socket 都是由一个四元组唯一标识的: (client_ip, client_port, server_ip, server_port)
    print(f"Connection established with {client_addr[0]}:{client_addr[1]}")
    print(f"Server Address: {conn_socket.getsockname()}")
    print(f"Client Address: {conn_socket.getpeername()}")
    try:
        while True:
            message = conn_socket.recv(2048)
            if not message:
                print(f"{client_addr} disconnected.")
                break
            print(f"Client -> {client_addr[0]}:{client_addr[1]} -> {message.decode()}")
            modified_message = message.decode().title()
            print(f"Server -> {client_addr[0]}:{client_addr[1]} -> {modified_message}\n")
            conn_socket.send(modified_message.encode())
    finally:
        conn_socket.close()


def main():
    """ A simple concurrent TCP server that handles multiple clients """
    server_name, server_port = '127.0.0.1', 18000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((server_name, server_port))
    server_socket.listen(2)
    print(f"Server is ready to receive connections on {server_name}:{server_port}")

    try:
        while True:
            # 客户端每次连接都会创建一个新的 conn_socket，然后创建一个线程来处理该连接
            conn_socket, client_addr = server_socket.accept()
            t = threading.Thread(target=handle_client, args=(conn_socket, client_addr))
            t.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()
        print("Server socket closed.")


if __name__ == "__main__":
    main()
