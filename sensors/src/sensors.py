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

channels = [AnalogIn(ads, ADS.P0), AnalogIn(
    ads, ADS.P1), AnalogIn(ads, ADS.P2)]
sensor_labels = ["Plant 1", "Plant 2", "Plant 3"]
logger.info("Soil moisture sensors connected.")

DRY_SATURATION = [None, None, None]
WET_SATURATION = [None, None, None]

CALIBRATION_FILE = 'config.json'

try:
    with open(CALIBRATION_FILE, 'r', encoding='UTF-8') as file:
        calibration_data = json.load(file)

    wet_saturation_data = calibration_data.get('wet_saturation')
    dry_saturation_data = calibration_data.get('dry_saturation')

    if wet_saturation_data and dry_saturation_data:
        for i in range(len(channels)):
            WET_SATURATION[i] = wet_saturation_data[i]
            DRY_SATURATION[i] = dry_saturation_data[i]

        logger.info('Calibration data loaded from the config file.')
        logger.info(calibration_data)

except FileNotFoundError:
    logger.info('Calibration file not found. Starting calibration process...')
    for i, channel in enumerate(channels):
        dry_check = input(
            f"Is Capacitive Sensor for {sensor_labels[i]} Dry? [y]: ")
        if dry_check.lower() == 'y':
            DRY_SATURATION[i] = channel.value
            logger.info("%5s\t%5s", 'raw', 'v')
            logger.info("%5d\t%5.3f", channel.value, channel.voltage)
        for x in range(0, 9):
            time.sleep(30)
            if channel.value > DRY_SATURATION[i]:
                DRY_SATURATION[i] = channel.value
            logger.info("%5d\t%5.3f", channel.value, channel.voltage)

        wet_check = input(
            f"Is Capacitive Sensor for {sensor_labels[i]} in Water? [y]: ")
        if wet_check.lower() == 'y':
            WET_SATURATION[i] = channel.value
            logger.info("%5s\t%5s", 'raw', 'v')
            logger.info("%5d\t%5.3f", channel.value, channel.voltage)
        for x in range(0, 9):
            time.sleep(30)
            if channel.value < WET_SATURATION[i]:
                WET_SATURATION[i] = channel.value
            logger.info("%5d\t%5.3f", channel.value, channel.voltage)

    config_data = {
        "sensors": []
    }

    for i in range(len(channels)):
        sensor_config = {
            "label": sensor_labels[i],
            "wet_saturation": WET_SATURATION[i],
            "dry_saturation": DRY_SATURATION[i]
        }
        config_data["sensors"].append(sensor_config)

    logger.info('Saving calibration data to the config file.')
    with open('config.json', 'w', encoding='UTF-8') as outfile:
        json.dump(config_data, outfile)
        logger.info(config_data)

logger.info("Starting sensors data logging...")

while True:
    try:
        today = datetime.date.today().strftime("%d-%m-%Y")
        DIRECTORY = "../data/"
        filename = f"{DIRECTORY}sensorsData_{today}.csv"

        os.makedirs(DIRECTORY, exist_ok=True)

        timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())

        SAMPLING_INTERVAL = 30

        sensor_readings = []
        for i, channel in enumerate(channels):
            soil_moisture_percentage = (
                channel.value - WET_SATURATION[i]) / (DRY_SATURATION[i]
                                                      - WET_SATURATION[i]) * 100
            sensor_readings.append(soil_moisture_percentage)

        with open(filename, "a", newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)

            header = ["Timestamp"] + [f"Soil Moisture ({label})" for label in sensor_labels] + [
                "Temperature", "Humidity"]

            values = [timestamp] + sensor_readings + \
                [bme280.temperature, bme280.relative_humidity]

            is_empty = csvfile.tell() == 0
            if is_empty:
                writer.writerow(header)
            writer.writerow(values)

        logger.info("Sensors values written to %s at %s.",
                    filename, timestamp)
        logger.info("Sensors values: %s", values)

        time.sleep(SAMPLING_INTERVAL)

    except IOError:
        logger.error(
            "An error occurred while logging the sensors data.", exc_info=True)

    except KeyboardInterrupt:
        logger.info('Exiting script.')
        break
