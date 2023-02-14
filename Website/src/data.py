"""Data collection script"""
from socket import socket, AF_INET, SOCK_STREAM

# Define the IP address and port to listen on
IP_ADDRESS = '192.168.0.119'
PORT = 20

# Create a socket object
soc = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the IP address and port
soc.connect((IP_ADDRESS, PORT))

# Listen for incoming connections
soc.listen()

# Accept a connection and receive data indefinitely
while True:
    # Accept a connection from a client
    client_socket, address = soc.accept()
    print(f'Connection from {address[0]}:{address[1]} has been established.')

    # Receive data from the client
    data = client_socket.recv(1024)

    # Print the received data
    print(f'Received data: {data.decode()}')

    # Close the connection
    client_socket.close()
