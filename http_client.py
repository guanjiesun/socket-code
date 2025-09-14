import socket
import threading

HOST    = '127.0.0.1'
PORT    = 9999
CHUNK   = 1024 * 4

def worker(path="/"):
    """ send request and receive response """
    # socket -> connect -> sendall -> recv -> close
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        # build request
        request = (
            f"GET {path} HTTP/1.1\r\n"
            "Host: localhost\r\n"
            "Connection: close\r\n"
            "User-Agent: DIY-Client\r\n"
            "\r\n"
        )

        # send request
        client.sendall(request.encode())

        # receive response
        response = b""
        while data := client.recv(CHUNK):
            response += data

        print(f"{response.decode()}", flush=True)

def main():
    """ A concurrent HTTP client based on Internet domain and TCP type socket"""
    paths = ["/", "/json"]
    threads = [threading.Thread(target=worker, args=(path,)) for path in paths]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
