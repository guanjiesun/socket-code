import socket
import threading

HOST = '0.0.0.0'
PORT = 18000

def handle_client(conn, client_addr):
    # 在 TCP 中，每一个 conn 都是由一个四元组唯一标识的: (client_ip, client_port, server_ip, PORT)
    client_addr = conn.getpeername()
    server_addr = conn.getsockname()
    print(f"[{threading.current_thread().name}] handling [client {client_addr}]")
    try:
        while True:
            message = conn.recv(2048)
            if not message:
                print(f"[Client {client_addr}] disconnected.")
                break
            print(f"[Client {client_addr}]: {message.decode()}")
            modified_message = message.decode().upper()
            print(f"[Server {server_addr}]: {modified_message}\n")
            conn.send(modified_message.encode())
    finally:
        conn.close()


def main():
    """一个"简单的 TCP 服务器，能够处理多个客户端连接，每个连接在独立的线程中处理"""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(2)
    print(f"Server is ready to receive connections on {HOST}:{PORT}\n") 

    threads = list()
    try:
        while True:
            # 客户端每次连接都会创建一个新的 conn，然后创建一个线程来处理该连接
            conn, client_addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, client_addr))
            t.start()
            threads.append(t)
    except KeyboardInterrupt:
        print("\nServer shutting down...")  # Ctrl+C 触发的异常
    finally:
        s.close()               # 关闭服务器套接字, 不再接受新的连接
        print("Server socket closed.")
        print("Waiting all threads to finish execution.")
        for t in threads:
            t.join()                        # 阻塞主线程, 直到所有以的子线程执行完毕
        print("All threads have finished execution.")


if __name__ == "__main__":
    print(f"[{threading.current_thread().name}] main thread starting...")
    main()
    print(f"[{threading.current_thread().name}] main thread exiting...")
