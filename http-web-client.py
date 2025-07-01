import socket


def main():
    """A simple HTTP client that connects to a server, sends a GET request, and prints the response."""

    HOST = '127.0.0.1'  # 服务器地址
    PORT = 9999         # 服务器端口

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # 构造 HTTP 请求
    request = (
        "GET / HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        "Connection: close\r\n"
        "User-Agent: MySimpleClient/1.0\r\n"
        "\r\n"
    )

    # 发送请求
    client_socket.sendall(request.encode())

    # 接收响应（分段读取直到 socket 关闭）
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    # 关闭连接
    client_socket.close()
    # 输出响应(包括状态行、头部和主体)
    print(response.decode())


if __name__ == "__main__":
    main()
