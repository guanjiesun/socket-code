import socket


def handle_client(client_socket):
    """处理客户端请求的函数"""
    try:
        while True:
            request = client_socket.recv(1024).decode()
            if not request:
                # 客户端端开连之后, 会发送一个空请求, 这时可以认为客户端已经断开连接
                print(f"[Client {client_socket.getpeername()}] disconnected.")
                break

            request_line = request.splitlines()[0]  # 获取请求行
            print(f"Request line: {request_line}")
            method, path, http_version = request_line.split()  # 解析请求行, 获取请求方法, 路径和 HTTP 版本

            if method == 'GET':
                if path in ['/', '/index.html']:
                    body = "<html><body><h1 style='color:red;'>Welcome to my web server!</h1></body></html>"
                else:
                    body = "<html><body><h1>404 Not Found</h1></body></html>"

                response = (
                    f"{http_version} 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                    "\r\n"
                    f"{body}"
                )
            else:
                body = "<h1>405 Method Not Allowed</h1>"
                response = (
                    f"{http_version} 405 Method Not Allowed\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                    "\r\n"
                    f"{body}"
                )
            client_socket.sendall(response.encode())
    finally:
        client_socket.close()
        print("Client socket closed.\n")


def main():
    """一个简单的 HTTP 服务器，能够处理 GET 请求"""

    server_name = '0.0.0.0'
    server_port = 9999
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # 创建 TCP 套接字
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许端口重用 
    server_socket.bind((server_name, server_port))                       # 绑定地址和端口
    server_socket.listen(5)                                              # 监听连接请求
    print(f"HTTP server is running on {server_name}:{server_port}...")

    try:
        while True:
            print("Waiting for a connection...")
            client_socket, client_addr = server_socket.accept()
            print(f"Connnection from: {client_addr[0]}:{client_addr[1]}")
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
