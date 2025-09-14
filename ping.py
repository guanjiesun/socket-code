import time
import socket

HOST        = "127.0.0.1"
PORT        = 13000
CHUNK_SIZE  = 1024 * 4

def main():
    """ ping client based on Internet domain and UDP type socket"""
    # socket -> settimeout -> sendto -> recvfrom -> close
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(5.0)
        try:
            for i in range(10):
                    message = f"Ping {i} from client".encode()
                    start = time.time()

                    s.sendto(message, (HOST, PORT))
                    received_message, server_address = s.recvfrom(CHUNK_SIZE)

                    end = time.time()
                    rtt = (end - start) * 1000
                    print(f"{len(received_message)} bytes from {server_address[0]}:{server_address[1]}: seq={i} time={rtt:.2f} ms")
        except socket.timeout:
            print("Request timed out, no response from server.\nIs the server running?\n")

if __name__ == '__main__':
    main()
