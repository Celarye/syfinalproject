import smbus2
import time

# Initialize I2C bus
bus = smbus2.SMBus(1)

# WPSE342 sensor address
address = 0x76

# Read temperature
def read_temperature():
    data = bus.read_i2c_block_data(address, 0xE3, 2)
    temp = ((data[0] << 8) + data[1]) / 100
    return temp

# Read humidity
def read_humidity():
    data = bus.read_i2c_block_data(address, 0xE5, 2)
    humidity = ((data[0] << 8) + data[1]) / 1024
    return humidity

# Read CO2
def read_CO2():
    data = bus.read_i2c_block_data(address, 0xE8, 2)
    CO2 = ((data[0] << 8) + data[1]) / 1024
    return CO2

# Read TVOC
def read_TVOC():
    data = bus.read_i2c_block_data(address, 0xE7, 2)
    TVOC = ((data[0] << 8) + data[1]) / 1024
    return TVOC

# Main loop
while True:
    temp = read_temperature()
    humidity = read_humidity()
    CO2 = read_CO2()
    TVOC = read_TVOC()

    print("Temperature:", temp, "C")
    print("Humidity:", humidity, "%")
    print("CO2:", CO2, "ppm")
    print("TVOC:", TVOC, "ppb")

    time.sleep(1)
