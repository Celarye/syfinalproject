"""WPSE342 Sensor"""
import time
import board
import busio
from board import *
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_ccs811

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
ccs =  adafruit_ccs811.CCS811(i2c)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25

while True:
    print("\nTemperature: %0.1f C" % bme280.temperature)
    print("Humidity: %0.1f %%" % bme280.relative_humidity)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    print("Altitude = %0.2f meters" % bme280.altitude)
    print("CO2: ", ccs.eco2, " TVOC:", ccs.tvoc)
    time.sleep(5)
