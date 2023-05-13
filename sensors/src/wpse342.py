import time
import board
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_ccs811

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
try:
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
except Exception as e:
    print(f"BME280 initialization error: {e}")

try:
    ccs811 = adafruit_ccs811.CCS811(i2c, address=0x5B)
except Exception as e:
    print(f"CCS811 initialization error: {e}")

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25

while True:
    try:
        print("\nTemperature: %0.1f C" % bme280.temperature)
        print("Humidity: %0.1f %%" % bme280.relative_humidity)
        print("Pressure: %0.1f hPa" % bme280.pressure)
        print("Altitude = %0.2f meters" % bme280.altitude)
        print("CO2: %1.0f PPM" % ccs811.eco2)
        print("TVOC: %1.0f PPM" % ccs811.tvoc)
        print("Temp: %0.1f C" % ccs811.temperature)
    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(5)
