import socket


server_name, server_port = 'localhost', 12000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(3)

while True:
    message = input('Input lowercase sentence: ')
    if message.lower() in ['exit', 'quit']:
        print('Exiting client...')
        break
    try:
        client_socket.sendto(message.encode(), (server_name, server_port))
        modified_message, server_address = client_socket.recvfrom(2048)
        print(f"{server_address[0]}:{server_address[1]} -> {modified_message.decode()}\n")
    except socket.timeout:
        print("Request timed out. No response from server. Is the server running?\n")

client_socket.close()
