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

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

i2c = board.I2C()

ads = ADS.ADS1015(i2c)

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
logger.info("BME280 connected.")

channel = AnalogIn(ads, ADS.P0)
logger.info("Soil moisture sensor connected.")

DRY_SATURATION = None
WET_SATURATION = None

CALIBRATION_FILE = 'config.json'

try:
    with open(CALIBRATION_FILE, 'r', encoding='UTF-8') as file:
        calibration_data = json.load(file)

    WET_SATURATION = calibration_data['wet_saturation']
    DRY_SATURATION = calibration_data['dry_saturation']

    logger.info('Calibration data loaded from the config file.')
    logger.info(calibration_data)

except FileNotFoundError:
    logger.info('Calibration file not found. Starting calibration process...')
    dry_check = input("Is Capacitive Sensor Dry? [y]: ")
    if dry_check.lower() == 'y':
        DRY_SATURATION = channel.value
        logger.info("%5s\t%5s", 'raw', 'v')
        logger.info("%5d\t%5.3f", channel.value, channel.voltage)
    for x in range(0, 9):
        time.sleep(30)
        if channel.value > DRY_SATURATION:
            DRY_SATURATION = channel.value
        logger.info("%5d\t%5.3f", channel.value, channel.voltage)

    wet_check = input("Is Capacitive Sensor in Water? [y]: ")
    if wet_check.lower() == 'y':
        WET_SATURATION = channel.value
        logger.info("%5s\t%5s", 'raw', 'v')
        logger.info("%5d\t%5.3f", channel.value, channel.voltage)
    for x in range(0, 9):
        time.sleep(30)
        if channel.value < WET_SATURATION:
            WET_SATURATION = channel.value
        logger.info("%5d\t%5.3f", channel.value, channel.voltage)

    config_data = {
        "wet_saturation": WET_SATURATION,
        "dry_saturation": DRY_SATURATION
    }

    logger.info('Saving calibration data to the config file.')
    with open('config.json', 'w', encoding='UTF-8') as outfile:
        json.dump(config_data, outfile)
        logger.info(config_data)

today = datetime.date.today().strftime("%d-%m-%y")
DIRECTORY = "../website/src/data/"
filename = f"{DIRECTORY}sensorData_{today}.csv"
SAMPLING_INTERVAL = 5

logger.info("Starting sensors data logging...")

os.makedirs(DIRECTORY, exist_ok=True)

while True:
    try:
        timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())

        soil_moisture_percentage = (channel.value - WET_SATURATION) / \
                           (DRY_SATURATION - WET_SATURATION) * 100

        with open(filename, "a", newline='', encoding='UTF-8') as csvfile:
            WRITER = csv.writer(csvfile)

            header = ["Timestamp", "Soil Moisture", "Temperature", "Humidity"]

            values = [timestamp, soil_moisture_percentage, bme280.temperature,
                      bme280.relative_humidity]

            is_empty = csvfile.tell() == 0
            if is_empty:
                WRITER.writerow(header)
            WRITER.writerow(values)

        logger.info("Sensors values written to %s at %s.", filename, timestamp)
        logger.info("Sensors values: %s", values)

        time.sleep(SAMPLING_INTERVAL)

    except IOError as error:
        logger.error("An error occurred while logging the sensors data.", exc_info=True)

    except KeyboardInterrupt:
        logger.info('Exiting script.')
        break
