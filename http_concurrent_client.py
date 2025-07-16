import socket
import threading


SERVER_ADDR = '127.0.0.1'  # 服务器地址
SERVER_PORT = 9999         # 服务器端口


def send_request(client_socket, path='/'):
    """发送 HTTP 请求并打印响应"""

    client_socket.connect((SERVER_ADDR, SERVER_PORT))

    # 构造 HTTP 请求
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {SERVER_ADDR}:{SERVER_PORT}\r\n"
        "Connection: close\r\n"
        "User-Agent: Guanjie's Client\r\n"
        "\r\n"
    )

    client_socket.sendall(request.encode())  # 发送请求
    response = client_socket.recv(1024)      # 接收响应
    print(f"\n[{threading.current_thread().name}]\n{response.decode()}")  # 打印服务器响应
    client_socket.close()                    # 关闭客户端套接字


def main():
    """一个可以并发请求的 HTTP 客户端，连接到 HTTP 服务器，发送请求并接收响应"""

    threads = list()
    paths = ['/index.html', '/json', '/forbidden']
    for path in paths:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        t = threading.Thread(target=send_request, args=(client_socket, path))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
