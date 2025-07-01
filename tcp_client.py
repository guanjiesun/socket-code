import socket


server_name, server_port = '127.0.0.1', 18000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_name, server_port))
# client_socket.settimeout(3)

while True:
    message = input('Input lowercase sentence (type quit or exit to interrupt TCP conncetion): ')
    if message.lower() in ['exit', 'quit']:
        print('Exiting client...')
        break
    client_socket.send(message.encode())
    modified_message = client_socket.recv(2048)
    print(f"{server_name}:{server_port}-> {modified_message.decode()}\n")

client_socket.close()
