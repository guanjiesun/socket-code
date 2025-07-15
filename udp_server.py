import socket
import threading


def handle_client(server_socket):
    """处理接收到的消息并返回修改后的消息"""
    message, client_address = server_socket.recvfrom(2048)
    print(f"[Client ({client_address[0]}:{client_address[1]})]: {message.decode()}")
    modified_message = message.decode().upper().encode()
    server_socket.sendto(modified_message, client_address)


def main():
    """一个简单的 UDP 服务器，处理客户端连接(单线程)"""

    server_port = 10000
    server_name = '0.0.0.0'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_name, server_port))
    print(f'[server {server_name}:{server_port}] is ready to receive...')

    try:
        while True:
            handle_client(server_socket)
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()
        print("Server socket closed.")


if __name__ == "__main__":
    print(f"[{threading.current_thread().name}] starting...")
    main()
    print(f"[{threading.current_thread().name}] ending...")
