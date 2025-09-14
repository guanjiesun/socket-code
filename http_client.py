import socket

HOST    = '127.0.0.1'
PORT    = 9999
CHUNK   = 1024 * 4

def main():
    """ A HTTP client based on UNIX domain and TCP type socket """
    # socket -> connect -> sendall -> recv -> close
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        # build request
        request = (
            "GET / HTTP/1.1\r\n"
            "Host: localhost\r\n"
            "Connection: close\r\n"
            "User-Agent: DIY-Client\r\n"
            "\r\n"
        )

        # send request
        client.sendall(request.encode())
        # receive response
        response = client.recv(1024)

        print(f"\n{response.decode()}")

if __name__ == "__main__":
    main()
