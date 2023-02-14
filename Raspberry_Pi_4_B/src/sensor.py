"""WPSE342 sensor script"""
import time
import socket
import smbus2

# Define the IP address and port of the receiving PC
IP_ADDRESS = '192.168.1.2'
PORT = 5555

# Initialize I2C bus
bus = smbus2.SMBus(1)

# WPSE342 sensor address
ADDRESS = 0x76

def read_temperature():
    """Read temperature."""
    data = bus.read_i2c_block_data(ADDRESS, 0xE3, 2)
    temp = ((data[0] << 8) + data[1]) / 100
    return temp

def read_humidity():
    """Read humidity."""
    data = bus.read_i2c_block_data(ADDRESS, 0xE5, 2)
    humidity = ((data[0] << 8) + data[1]) / 1024
    return humidity

def read_co2():
    """Read CO2."""
    data = bus.read_i2c_block_data(ADDRESS, 0xE8, 2)
    co2 = ((data[0] << 8) + data[1]) / 1024
    return co2

def read_tvoc():
    """Read TVOC."""
    data = bus.read_i2c_block_data(ADDRESS, 0xE7, 2)
    tvoc = ((data[0] << 8) + data[1]) / 1024
    return tvoc

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect((IP_ADDRESS, PORT))

# Main loop
while True:
    finaltemp = read_temperature()
    finalhumidity = read_humidity()
    finalCO2 = read_co2()()
    finalTVOC = read_tvoc()

    # Construct a message with the data
    message = f'Temperature: {finaltemp} C, Humidity: {finalhumidity}%, CO2: {finalCO2} ppm, TVOC: {finalTVOC} ppb'

    # Send the message to the server
    s.send(message.encode())

    time.sleep(300)
