import socket
import threading
import uuid
import json

SERVER_NAME = '0.0.0.0'
SERVER_PORT = 9999
CHUNK = 1024 * 4

def handle_client(conn, addr):
    """处理客户端请求的函数"""
    print(f"[{threading.current_thread().name}] [client {addr}]")

    request = b""
    while b"\r\n\r\n" not in request:
        data = conn.recv(CHUNK)
        if not data:
            break
        request += data

    headers = request.split("\r\n")
    request_line = headers[0]
    method, path, http_version = request_line.split(' ', maxsplit=2)

    if method == 'GET':
        if path == '/' or path == '/index.html':
            status_code = 200
            reason_phrase = 'OK'
            body = "<html><body><h1 style='color:red;'>Welcome to my web server!</h1></body></html>"
            content_type = 'text/html; charset=utf-8'
        elif path == '/json':
            status_code = 200
            reason_phrase = 'OK'
            data = {
                "message": "hello from json",
                "session_id": str(uuid.uuid4()),
                "status": "success",
            }
            body = json.dumps(data)
            content_type = 'application/json; charset=utf-8'
        elif path == '/forbidden':
            status_code = 403
            reason_phrase = 'Forbidden'
            body = "<html><body><h1>403 Forbidden</h1></body></html>"
            content_type = 'text/html; charset=utf-8'
        elif path == '/not-found':
            status_code = 404
            reason_phrase = 'Not Found'
            body = "<html><body><h1>404 Not Found</h1></body></html>"
            content_type = 'text/html; charset=utf-8'
        else:
            status_code = 204
            reason_phrase = 'No Content'
            body = ""
            content_type = 'text/html; charset=utf-8'

        response = (
            f"{http_version} {status_code} {reason_phrase}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
            f"Set-Cookie: sessionid={str(uuid.uuid4())}; Max-Age=5\r\n"
            "\r\n"
            f"{body}"
        )
    else:
        status_code = 405
        reason_phrase = 'Method Not Allowed'
        body = "<h1>405 Method Not Allowed</h1>"
        content_type = 'text/html; charset=utf-8'
        response = (
            f"{http_version} {status_code} {reason_phrase}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            "Connection: keep-alive\r\n"
            f"Set-Cookie: sessionid={str(uuid.uuid4())}; Max-Age=5\r\n"
            "\r\n"
            f"{body}"
        )
    conn.sendall(response.encode())
    conn.close()


def main():
    """ A concurrent HTTP server handles GET reqeust """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # 创建 TCP 套接字
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许端口重用 
    s.bind((SERVER_NAME, SERVER_PORT))                       # 绑定地址和端口
    s.listen(5)                                              # 监听连接请求
    print(f"Server listening on {SERVER_NAME}:{SERVER_PORT}...\n")

    threads = list()
    try:
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()
            threads.append(t)
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        s.close()
        print("Server socket closed.")
        print("Waiting all threads to finish execution.")
        for t in threads:
            t.join()
        print("All threads have finished execution.")


if __name__ == '__main__':
    main()
