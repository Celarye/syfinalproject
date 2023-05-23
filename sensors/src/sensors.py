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
from flask import Flask, send_file

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

logger.info("Starting sensors data logging...")

app = Flask(__name__)


@app.route('/data/sensorsData_<date>.csv')
def serve_csv():
    """Serves the CSV using Flask"""
    today = datetime.date.today().strftime("%d-%m-%Y")
    directory = "../data"
    filename = f"{directory}/sensorsData_{today}.csv"

    os.makedirs(directory, exist_ok=True)

    timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())

    sampling_interval = 30

    soil_moisture_percentage = (
        channel.value - WET_SATURATION) / (DRY_SATURATION - WET_SATURATION) * 100

    with open(filename, "a", newline='', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)

        header = ["Timestamp", "Soil Moisture", "Temperature", "Humidity"]

        values = [timestamp, soil_moisture_percentage,
                  bme280.temperature, bme280.relative_humidity]

        is_empty = csvfile.tell() == 0
        if is_empty:
            writer.writerow(header)
        writer.writerow(values)

    logger.info("Sensors values written to %s at %s.", filename, timestamp)
    logger.info("Sensors values: %s", values)

    time.sleep(sampling_interval)

    return send_file(filename, as_attachment=True, attachment_filename=f'sensorsData_{today}.csv')


if __name__ == '__main__':
    app.run()
