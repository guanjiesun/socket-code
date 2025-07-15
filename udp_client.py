import socket


def main():
    """一个简单的 UDP 客户端，连接到服务器，发送消息并接收响应"""

    server_name = '127.0.0.1'
    server_port = 10000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(2)

    while True:
        message = input('Input lowercase sentence: ')
        if message.lower() in ['exit', 'quit']:
            print('Exiting client...')
            break
        try:
            client_socket.sendto(message.encode(), (server_name, server_port))
            modified_message, server_address = client_socket.recvfrom(1024)
            print(f"[{server_address[0]}:{server_address[1]}]: {modified_message.decode()}\n")
        except socket.timeout:
            print("Request timed out. No response from server. Is the server running?\n")

    client_socket.close()


if __name__ == "__main__":
    main()
