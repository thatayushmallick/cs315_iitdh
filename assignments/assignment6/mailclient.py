import socket
import ssl
from base64 import b64encode

# User credentials and email details
userEmail = "220010008@iitdh.ac.in"
userPassword = ""  # Use the generated app password
userDestinationEmail = input("Enter Email Destination: ")
userSubject = input("Enter Subject: ")
userBody = input("Enter Message: ")

# msg = '{}.\r\n I love computer networks!'.format(userBody)
msg = f"Subject: {userSubject}\r\nFrom: {userEmail}\r\nTo: {userDestinationEmail}\r\n\r\n{userBody}\r\n I love computer networks!"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(mailserver)

# Receive and check server response
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print("220 reply not received from server.")

# Send HELO command and print server response.
heloCommand = "HELO Alice\r\n"
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print("250 reply not received from server.")

#account authentication
clientSocket.send("STARTTLS\r\n".encode())
clientSocket.recv(1024)

# sslClientSocket = ssl.wrap_socket(clientSocket)   # deprecated in newer versions of python
context = ssl.create_default_context()
sslClientSocket = context.wrap_socket(clientSocket, server_hostname="smtp.gmail.com")

sslClientSocket.send("AUTH LOGIN\r\n".encode())
print(sslClientSocket.recv(1024))
sslClientSocket.send(b64encode(userEmail.encode()) + "\r\n".encode())
print(sslClientSocket.recv(1024))
sslClientSocket.send(b64encode(userPassword.encode()) + "\r\n".encode())
print(sslClientSocket.recv(1024))

# Send MAIL FROM command and print server response.
mailFromCommand = f"MAIL FROM:<{userEmail}>\r\n"
sslClientSocket.send(mailFromCommand.encode())
recv3 = sslClientSocket.recv(1024).decode()
print(recv3)

# Send RCPT TO command and print server response.
rcptToCommand = f"RCPT TO:<{userDestinationEmail}>\r\n"
sslClientSocket.send(rcptToCommand.encode())
recv4 = sslClientSocket.recv(1024).decode()
print(recv4)

# Send DATA command and print server response.
sslClientSocket.send("DATA\r\n".encode())
recv5 = sslClientSocket.recv(1024).decode()
print(recv5)

# Send message data.
sslClientSocket.send(msg.encode())

# Message ends with a single period.
sslClientSocket.send("\r\n.\r\n".encode())
recv6 = sslClientSocket.recv(1024).decode()
print(recv6)

# Send QUIT command and get server response.
sslClientSocket.send("QUIT\r\n".encode())
recv7 = sslClientSocket.recv(1024).decode()
print(recv7)

# Close connection
sslClientSocket.close()
