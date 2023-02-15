"""WPSE342 sensor Raspberry Pi 4 B script"""
import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_ccs811

# Initialize I2C bus and sensors
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
ccs811 = adafruit_ccs811.CCS811(i2c)

# Wait for sensors to be ready
while not ccs811.data_ready:
    pass

while not bme280.data_ready:
    pass

try:
    # Read sensor data
    ccs811_data = ccs811.read()
    bme280_data = bme280.measure()

    # Print sensor data
    print(f"CO2: {ccs811_data['co2']} ppm")
    print(f"TVOC: {ccs811_data['tvoc']} ppb")
    print(f"Temperature: {bme280_data.temperature:.1f} C")
    print(f"Humidity: {bme280_data.humidity:.1f} %")
    print(f"Pressure: {bme280_data.pressure:.1f} hPa")

    # code that may raise exceptions
except OSError as e:
    # handle I/O errors
    print(f"I/O error: {e}")
except ValueError as e:
    # handle data conversion errors
    print(f"Data conversion error: {e}")
except Exception as e:
    # handle other unexpected exceptions
    print(f"Unexpected error: {e}")

# Wait 5 minutes before taking the next reading
time.sleep(300)
