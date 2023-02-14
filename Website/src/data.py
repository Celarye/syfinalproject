"""Data collection script"""
import socket

# Define the IP address and port to listen on
IP_ADDRESS = '192.168.0.255'
PORT = 6776

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port
s.bind((IP_ADDRESS, PORT))

# Listen for incoming connections
s.listen()

# Accept a connection and receive data indefinitely
while True:
    # Accept a connection from a client
    client_socket, address = s.accept()
    print(f'Connection from {address[0]}:{address[1]} has been established.')

    # Receive data from the client
    data = client_socket.recv(1024)

    # Print the received data
    print(f'Received data: {data.decode()}')

    # Close the connection
    client_socket.close()
