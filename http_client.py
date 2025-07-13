import socket


def main():
    """A simple HTTP client that connects to a server, sends a GET request, and prints the response."""

    server_addr = '127.0.0.1'  # 服务器地址
    server_port = 9999         # 服务器端口

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_addr, server_port))

    # 构造 HTTP 请求
    request = (
        "GET / HTTP/1.1\r\n"
        f"Host: {server_addr}:{server_port}\r\n"
        "Connection: keep-alive\r\n"
        "User-Agent: Guanjie's Client\r\n"
        "\r\n"
    )

    client_socket.sendall(request.encode())  # 发送请求
    response = client_socket.recv(1024)      # 接收响应
    print(f"\n{response.decode()}")          # 打印服务器响应

    client_socket.close()                    # 关闭客户端套接字


if __name__ == "__main__":
    main()
