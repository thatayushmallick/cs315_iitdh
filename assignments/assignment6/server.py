import socket

# Server Configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345      # Port to bind to

# Create and bind the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")
    
    # Open a file to store received data
    with open("received.txt", "wb") as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)

    print("File received successfully")
    
    # Read the received file and extract the first and last 10 lines
    with open("received.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        first_10 = lines[:10]
        last_10 = lines[-10:]
        response = "".join(first_10 + last_10)
    
    # Send the extracted lines back to the client
    conn.sendall(response.encode())
    print("Sent first and last 10 lines back to the client")
    
    # Close connection
    conn.close()
    print("Connection closed\n")

    # Exit after one transaction (modify for continuous listening)
    break

server_socket.close()
