import socket
import threading

# Server configuration
HOST = '172.20.10.4'  # Bind to all available interfaces
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received: {message}")

            # Broadcast the message to all other clients
            for client in clients:
                if client != client_socket:
                    try:
                        client.sendall(message.encode())
                    except Exception as e:
                        print(f"Error sending to client: {e}")
                        clients.remove(client)
        except Exception as e:
            print(f"Error: {e}")
            break

    clients.remove(client_socket)
    client_socket.close()

def accept_connections():
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

print("Server is listening...")
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
