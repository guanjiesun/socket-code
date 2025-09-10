import socket

SERVER_ADDR = '127.0.0.1'
PORT        = 18000
CHUNK_SIZE  = 1024 * 4

def main():
    """ 基于 AF_INET and TCP 的 echo 客户端 """
    # socket -> s.connect -> s.sendall -> s.shutdown -> loop s.recv -> s.close
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_ADDR, PORT))
        s.sendall(b"hello")
        s.shutdown(socket.SHUT_WR)  # if without this line code, the server and client will be deadlocked!

        response = b""
        while data := s.recv(CHUNK_SIZE):
            response += data
        print(response.decode())

if __name__ == "__main__":
    main()
