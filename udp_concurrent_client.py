import socket
import threading

SERVER_NAME = '127.0.0.1'
SERVER_PORT = 10000

def send_message(client_socket, msg):
    """发送消息并接收响应"""

    client_socket.sendto(msg.encode(), (SERVER_NAME, SERVER_PORT))
    modified_msg, server_addr = client_socket.recvfrom(1024)
    print(f"[{threading.current_thread().name}] [Server {server_addr[0]}:{server_addr[1]}]: {modified_msg.decode()}\n")
    client_socket.close()


def main():
    """一个可以并发请求的 UDP 客户端，连接到 UDP 服务器，发送消息并接收响应"""

    threads = list()
    messages = list('abcdefg')

    for message in messages:
        # 创建 len(messages) 个线程，每个线程发送 message
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        t = threading.Thread(target=send_message, args=(client_socket, message))
        t.start()
        threads.append(t)

    for t in threads:
        # 等待子线程结束
        t.join()


if __name__ == "__main__":
    print(f"[{threading.current_thread().name}] starting...")
    main()
    print(f"[{threading.current_thread().name}] ending...")
