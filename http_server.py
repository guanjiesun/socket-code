import uuid
import json
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

HOST = '0.0.0.0'
PORT = 9999
CHUNK = 1024 * 4

def handle_client(conn, addr):
    """ Handle request from client using conn socket """
    # receive the request
    request = b""
    while b"\r\n\r\n" not in request:
        data = conn.recv(CHUNK)
        if not data:
            break
        request += data

    # parse the request
    headers = request.decode().split("\r\n")
    request_line = headers[0]
    method, path, http_version = request_line.split(' ', maxsplit=2)

    # log on stdin
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] {addr[0]}:{addr[1]} {method} {path} {http_version}", flush=True)

    # build response
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
        # Only GET request is allowed
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

    # send response and close the conn socket
    conn.sendall(response.encode())
    conn.close()


def main():
    """ A concurrent HTTP server handles GET reqeust """
    # socket -> bind -> listen -> accept -> close
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"\nServer listening on {HOST}:{PORT}...\n")

        with ThreadPoolExecutor(max_workers=16) as executor:
            try:
                while True:
                    conn, addr = s.accept()
                    executor.submit(handle_client, conn, addr)
            except KeyboardInterrupt:
                print("\nServer shutting down...", flush=True)

if __name__ == '__main__':
    main()
