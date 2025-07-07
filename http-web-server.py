import socket


HOST = '0.0.0.0'
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server in running, listen port {PORT}...")


# A simple HTTP server that handles GET requests
try:
    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"\nConnnection from: {client_addr[0]}:{client_addr[1]}")
        try:
            request = client_socket.recv(1024).decode()
            request_line = request.splitlines()[0]
            print(f"Request line: {request_line}")
            method, path, http_version = request_line.split()

            if method == 'GET':
                if path in ['/', '/index.html']:
                    body = "<html><body><h1 style='color:red;'>Welcome to my web server!</h1></body></html>"
                else:
                    body = "<html><body><h1>404 Not Found</h1></body></html>"

                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                    "\r\n"
                    f"{body}"
                )
                response = response.encode()
                if path == '/dog':
                    with open("./sources/dog.jpg", "rb") as f:
                        image_data = f.read()

                    response_header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: image/jpeg\r\n"
                        f"Content-Length: {len(image_data)}\r\n"
                        "\r\n"
                    )
                    response = response_header.encode() + image_data
                client_socket.sendall(response)
            else:
                response = (
                    "HTTP/1.1 405 Method Not Allowed\r\n"
                    "Content-Type: text/html\r\n"
                    "\r\n"
                    "<h1>405 Method Not Allowed</h1>"
                )
                client_socket.sendall(response.encode())
        finally:
            client_socket.close()
except KeyboardInterrupt:
    print("Server shutting down...")
finally:
    server_socket.close()
