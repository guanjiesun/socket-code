import socket
import threading
import uuid


SERVER_NAME = '0.0.0.0'
SERVER_PORT = 9999


def handle_client(conn_sock):
    """处理客户端请求的函数"""
    client_addr = conn_sock.getpeername()
    print(f"[{threading.current_thread().name}] [client {client_addr}]")

    try:
        while True:
            request = conn_sock.recv(1024).decode()
            if not request:
                # 客户端端开连之后, 会发送一个空请求, 这时可以认为客户端已经断开连接
                print(f"[{threading.current_thread().name}] [Client {client_addr}] disconnected.")
                break

            request_line = request.splitlines()[0]             # 获取请求行
            method, path, http_version = request_line.split()  # 解析请求行, 获取请求方法, 路径和 HTTP 版本

            if method == 'GET':
                if path in ['/', '/index.html']:
                    status_code = 200
                    reason_phrase = 'OK'
                    body = "<html><body><h1 style='color:red;'>Welcome to my web server!</h1></body></html>"
                else:
                    status_code = 404
                    reason_phrase = 'Not Found'
                    body = "<html><body><h1>404 Not Found</h1></body></html>"

                response = (
                    f"{http_version} {status_code} {reason_phrase}\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                    f"Set-Cookie: sessionid={str(uuid.uuid4())}; Max-Age=5\r\n"
                    "Connection: keep-alive\r\n"
                    "\r\n"
                    f"{body}"
                )
            else:
                status_code = 405
                reason_phrase = 'Method Not Allowed'
                body = "<h1>405 Method Not Allowed</h1>"
                response = (
                    f"{http_version} {status_code} {reason_phrase}\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                    f"Set-Cookie: sessionid={str(uuid.uuid4())}; Max-Age=5\r\n"
                    "Connection: keep-alive\r\n"
                    "\r\n"
                    f"{body}"
                )
            conn_sock.sendall(response.encode())
    finally:
        conn_sock.close()


def main():
    """一个简单的 HTTP 并发服务器, 能够处理 GET 请求"""

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # 创建 TCP 套接字
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许端口重用 
    server_socket.bind((SERVER_NAME, SERVER_PORT))                       # 绑定地址和端口
    server_socket.listen(5)                                              # 监听连接请求
    print(f"HTTP server is running on {SERVER_NAME}:{SERVER_PORT}...\n")

    threads = list()
    try:
        while True:
            conn_sock, client_addr = server_socket.accept()
            t = threading.Thread(target=handle_client, args=(conn_sock,))
            t.start()
            threads.append(t)
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()
        print("Server socket closed.")
        print("Waiting all threads to finish execution.")
        for t in threads:
            t.join()
        print("All threads have finished execution.")


if __name__ == '__main__':
    print(f"{threading.current_thread().name} starting...")
    main()
    print(f"{threading.current_thread().name} ending...")
