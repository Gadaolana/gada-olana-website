import socket
import threading

# Server configuration
HOST = '172.20.10.4'  # Bind to all available interfaces
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to local host and port
server_socket.bind((HOST, PORT))

# Enable server to accept connections
server_socket.listen(5)

clients = []

def handle_client(client_socket):
    while True:
        try:
            # Receive message from client
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

    # Remove and close the client socket on disconnect
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
