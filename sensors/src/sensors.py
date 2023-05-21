"""Sensors Script"""
import os
import time
import datetime
import json
import csv
import logging
import board
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_bme280 import basic as adafruit_bme280

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')  # Updated format
logger = logging.getLogger(__name__)

# Create the I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create the BME280 and the CCS811 sensor objects
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
logger.info("BME280 connected.")

# Create a single-ended input for the soil moisture sensor (channel 0)
channel = AnalogIn(ads, ADS.P0)
logger.info("Soil moisture sensor connected.")

MAX_VAL = None
MIN_VAL = None
bme280.sea_level_pressure = 1013.25  # Default pressure (hPa) at sea level

# Load calibration data from the JSON file if it exists
CALIBRATION_FILE = 'config.json'

try:
    with open(CALIBRATION_FILE, 'r', encoding='UTF-8') as file:
        calibration_data = json.load(file)

    MIN_VAL = calibration_data['full_saturation']
    MAX_VAL = calibration_data['zero_saturation']
    bme280.sea_level_pressure = calibration_data['air_pressure']

    logger.info('Calibration data loaded from the config file.')
    logger.info(calibration_data)

except FileNotFoundError:
    logger.info('Calibration file not found. Starting calibration process...')
    # Calibration for the sensor
    baseline_check = input("Is Capacitive Sensor Dry? (enter 'y' to proceed): ")
    if baseline_check.lower() == 'y':
        MAX_VAL = channel.value
        logger.info(f"------{'raw':>5}\t{'v':>5}")
    for x in range(0, 10):
        if channel.value > MAX_VAL:
            logger.info(f"{channel.value:>5}\t{channel.voltage:>5.3f}")
            time.sleep(0.5)
            logger.info('\n')

    water_check = input("Is Capacitive Sensor in Water? (enter 'y' to proceed): ")
    if water_check.lower() == 'y':
        MIN_VAL = channel.value
        logger.info(f"------{'raw':>5}\t{'v':>5}")
    for x in range(0, 10):
        if channel.value < MIN_VAL:
            MIN_VAL = channel.value
            logger.info(f"{channel.value:>5}\t{channel.voltage:>5.3f}")
            time.sleep(0.5)
            logger.info('\n')

    air_pressure = float(input("Enter the current air pressure (hPa): "))

    # Create a dictionary with calibration data
    config_data = {
        "full_saturation": MIN_VAL,
        "zero_saturation": MAX_VAL,
        "air_pressure": air_pressure
    }

    # Save calibration data to a JSON file
    logger.info('Saving calibration data to the config file.')
    with open('config.json', 'w', encoding='UTF-8') as outfile:
        json.dump(config_data, outfile)
        logger.info('\n')
        logger.info(config_data)
        time.sleep(0.5)

# Continuous reading and writing of moisture values
today = datetime.date.today().strftime("%d-%m-%y")
directory = "../website/data/"
filename = f"{directory}sensorData_{today}.csv"
SAMPLING_INTERVAL = 5  # Interval between readings in seconds

logger.info("Starting sensor data logging...")

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

while True:
    try:
        TIMESTAMP = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())

        with open(filename, "a", newline='', encoding='UTF-8') as csvfile:
            WRITER = csv.writer(csvfile)

            header = ["Timestamp", "Sensor Value", "Sensor Voltage", "Temperature", "Humidity",
                      "Pressure", "Altitude"]

            values = [TIMESTAMP, channel.value, channel.voltage, bme280.temperature,
                      bme280.relative_humidity, bme280.pressure, bme280.altitude]

            # Check if the file is empty (no header present)
            is_empty = csvfile.tell() == 0
            if is_empty:
                WRITER.writerow(header)
            WRITER.writerow(values)

        logger.info(f"Sensor values written to {filename} at {TIMESTAMP}.")
        logger.info(f"Sensor values: {values}")  # Log values in console
        time.sleep(SAMPLING_INTERVAL)

    except Exception as error:
        logger.error("An error occurred while logging sensor data.", exc_info=True)

    except KeyboardInterrupt:
        logger.info('Exiting script.')
        break
