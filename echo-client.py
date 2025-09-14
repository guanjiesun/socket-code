import socket
import threading

SERVER_ADDR = '127.0.0.1'
PORT        = 18000
CHUNK_SIZE  = 1024 * 4

def worker(msg):
    """ create a socket based on Internet domain and TCP type """
    # socket -> s.connect -> s.sendall -> s.shutdown -> s.recv -> s.close
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_ADDR, PORT))
        s.sendall(msg)
        # if without shutdown, the server and client will be deadlocked!
        s.shutdown(socket.SHUT_WR)

        response = b""
        while data := s.recv(CHUNK_SIZE):
            response += data
        print("OUTPUT:", response.decode(), flush=True)

def main():
    """ echo client """
    while True:
        try:
            msg = input("INPUT : ").encode()
        except KeyboardInterrupt:
            print()
            break
        else:
            t = threading.Thread(target=worker, args=(msg,))
            t.start()
            t.join()

if __name__ == "__main__":
    main()
