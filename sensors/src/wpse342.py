"""WPSE342 Sensor"""
import time
import board
import busio
import adafruit_bme280
import adafruit_ccs811

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
ccs811 = adafruit_ccs811.CCS811(i2c)

while True:
    temperature = bme280.temperature
    humidity = bme280.humidity
    tvoc = ccs811.tvoc
    eco2 = ccs811.eco2

    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("TVOC:", tvoc)
    print("eCO2:", eco2)

    time.sleep(1)
