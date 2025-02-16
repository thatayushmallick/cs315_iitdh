import socket

# Server Configuration
HOST = '127.0.0.1'  # Server IP (localhost for testing)
PORT = 12345        # Must match the server's port

# Create a client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to server at {HOST}:{PORT}")

# Open and send the file in chunks
with open("alice.txt", "rb") as f:
    while chunk := f.read(1024):
        client_socket.sendall(chunk)

# Signal end of transmission
client_socket.shutdown(socket.SHUT_WR)

# Receive and display the response from the server
response = client_socket.recv(4096).decode()
print("Received from server:\n", response)

# Close the connection
client_socket.close()
