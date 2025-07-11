import socket
import threading


def handle_client(conn_socket, client_addr):
    # 在 TCP 中，每一个 conn_socket 都是由一个四元组唯一标识的: (client_ip, client_port, server_ip, server_port)
    client_addr = conn_socket.getpeername()
    server_addr = conn_socket.getsockname()
    print(f"[{threading.current_thread().name}] handling client")
    print(f"Connection established with {client_addr[0]}:{client_addr[1]}")
    try:
        while True:
            message = conn_socket.recv(2048)
            if not message:
                print(f"Client {client_addr} disconnected.")
                break
            print(f"[Client {client_addr}]: {message.decode()}")
            modified_message = message.decode().upper()
            print(f"[Server {server_addr}]: {modified_message}\n")
            conn_socket.send(modified_message.encode())
    finally:
        conn_socket.close()


def main():
    """一个"简单的 TCP 服务器，能够处理多个客户端连接，每个连接在独立的线程中处理"""

    server_name, server_port = '127.0.0.1', 18000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((server_name, server_port))
    server_socket.listen(2)
    print(f"Server is ready to receive connections on {server_name}:{server_port}\n") 

    threads = list()
    try:
        while True:
            # 客户端每次连接都会创建一个新的 conn_socket，然后创建一个线程来处理该连接
            conn_socket, client_addr = server_socket.accept()
            t = threading.Thread(target=handle_client, args=(conn_socket, client_addr))
            t.start()
            threads.append(t)
    except KeyboardInterrupt:
        print("\nServer shutting down...")  # Ctrl+C 触发的异常
    finally:
        server_socket.close()  # 关闭服务器套接字, 不再接受新的连接
        print("Server socket closed.")
        for t in threads:
            t.join()  # 阻塞主线程, 直到所有以的子线程执行完毕
        print("All threads have finished execution.")


if __name__ == "__main__":
    print(f"[{threading.current_thread().name}] main thread starting...")
    main()
    print(f"[{threading.current_thread().name}] main thread exiting...")
