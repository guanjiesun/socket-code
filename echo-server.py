import socket

HOST = '0.0.0.0'
PORT = 18000
BACKLOG = 16
CHUNK_SIZE = 1024 * 4

def handle_client(conn, addr):
    with conn:
        print(f"{addr[0]}:{addr[1]}", flush=True, end=' ')

        request = b""
        while data := conn.recv(CHUNK_SIZE):
            request += data
        print(request.decode(), flush=True)

        conn.sendall(request.decode()[::-1].encode())

def main():
    """ 基于 AF_INET and TCP 的 echo 服务器 """
    # socket -> s.bind -> s.listen -> s.accept -> s.close
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(BACKLOG)
        print(f"Listening on {HOST}:{PORT}\n", flush=True) 

        try:
            while True:
                conn, addr = s.accept()
                handle_client(conn, addr)
        except KeyboardInterrupt:
            print("\nServer shutting down...")

if __name__ == "__main__":
    main()