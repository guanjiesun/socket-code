import socket


def main():
    """一个简单的 TCP 客户端，连接到服务器，发送消息并接收响应"""

    server_name, server_port = '127.0.0.1', 18000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, server_port))

    try:
        print('Type quit or exit to close TCP conncetion!')
        while True:
            message = input('Input your message: ')  # 输入消息
            if message.lower() in ['exit', 'quit']:
                print('Exiting client...')
                break
            client_socket.send(message.encode())  # 发送消息
            modified_message = client_socket.recv(2048)  # 接收服务器响应
            print(f"{server_name}, {server_port}: {modified_message.decode()}\n")  # 打印响应
    except KeyboardInterrupt:
        print("\nClient shutting down...")  # Ctrl+C 触发的异常
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
