import socket
import time


server_ip, server_port = '127.0.0.1', 13000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1)

for i in range(10):
    try:
        message = f"Ping {i} from client"
        start = time.time()
        client_socket.sendto(message.encode(), (server_ip, server_port))
        received_message, server_address = client_socket.recvfrom(2048)
        end = time.time()
        rtt = (end - start) * 1000
        print(f"{len(received_message)} bytes from {server_address[0]}:{server_address[1]} -> RTT = {rtt:.2f} ms")
    except socket.timeout:
        print("Request timed out. No response from server. Is the server running?\n")

client_socket.close()
