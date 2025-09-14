import socket

CHUNK_SIZE = 2048
HOST = "127.0.0.1"
PORT = 13000

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print('Server is ready to receive...')
        try:
            while True:
                msg, addr = s.recvfrom(CHUNK_SIZE)
                print(f"[{addr[0]}:{addr[1]}]: {msg.decode()}", flush=True)
                ret = f"Pong from server: {msg.decode()}".encode()
                s.sendto(ret, addr)
        except KeyboardInterrupt:
            print("\nServer shutting down...")

if __name__ == '__main__':
    main()