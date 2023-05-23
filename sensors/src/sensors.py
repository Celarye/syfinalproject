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

NUM_TRACKED_PLANTS = None

CALIBRATION_FILE = 'config.json'

if not os.path.isfile(CALIBRATION_FILE):
    num_tracked_plants = input("Enter the number of tracked plants (1-3): ")
    NUM_TRACKED_PLANTS = int(num_tracked_plants)
else:
    with open(CALIBRATION_FILE, 'r', encoding='UTF-8') as file:
        calibration_data = json.load(file)

    if 'num_tracked_plants' in calibration_data:
        logger.info("Number of tracked plants: %s",
                    calibration_data['num_tracked_plants'])
        update_num_plants = input(
            "Do you want to update the number of tracked plants? [y/n]: ")
        if update_num_plants.lower() == 'y':
            num_tracked_plants = input(
                "Enter the new number of tracked plants (1-3): ")
            NUM_TRACKED_PLANTS = int(num_tracked_plants)
        else:
            NUM_TRACKED_PLANTS = calibration_data['num_tracked_plants']
    else:
        num_tracked_plants = input(
            "Enter the number of tracked plants (1-3): ")
        NUM_TRACKED_PLANTS = int(num_tracked_plants)

channels = [AnalogIn(ads, getattr(ADS, f'P{i}'))
            for i in range(NUM_TRACKED_PLANTS)]
logger.info("Soil moisture sensor(s) connected.")

try:
    with open(CALIBRATION_FILE, 'r', encoding='UTF-8') as file:
        calibration_data = json.load(file)

    if 'num_tracked_plants' in calibration_data and \
            calibration_data['num_tracked_plants'] == NUM_TRACKED_PLANTS:
        for i in range(NUM_TRACKED_PLANTS):
            wet_saturation = calibration_data['plants'][i]['wet_saturation']
            dry_saturation = calibration_data['plants'][i]['dry_saturation']
            setattr(channels[i], 'wet_saturation', wet_saturation)
            setattr(channels[i], 'dry_saturation', dry_saturation)
    else:
        logger.info(
            'Calibration data mismatch. Starting calibration process...')

except FileNotFoundError:
    logger.info('Calibration file not found. Starting calibration process...')

    for i in range(NUM_TRACKED_PLANTS):
        logger.info("Calibrating soil moisture sensor for Plant %d...", i + 1)

        dry_check = input(f"Is Capacitive Sensor Dry for Plant {i + 1}? [y]: ")
        if dry_check.lower() == 'y':
            setattr(channels[i], 'dry_saturation', channels[i].value)
            logger.info("%5s\t%5s", 'raw', 'v')
            logger.info("%5d\t%5.3f", channels[i].value, channels[i].voltage)

        for x in range(0, 9):
            time.sleep(30)
            if channels[i].value > getattr(channels[i], 'dry_saturation'):
                setattr(channels[i], 'dry_saturation', channels[i].value)
            logger.info("%5d\t%5.3f", channels[i].value, channels[i].voltage)

        wet_check = input(
            f"Is Capacitive Sensor in Water for Plant {i + 1}? [y]: ")
        if wet_check.lower() == 'y':
            setattr(channels[i], 'wet_saturation', channels[i].value)
            logger.info("%5s\t%5s", 'raw', 'v')
            logger.info("%5d\t%5.3f", channels[i].value, channels[i].voltage)

        for x in range(0, 9):
            time.sleep(30)
            if channels[i].value < getattr(channels[i], 'wet_saturation'):
                setattr(channels[i], 'wet_saturation', channels[i].value)
            logger.info("%5d\t%5.3f", channels[i].value, channels[i].voltage)

    config_data = {
        "num_tracked_plants": NUM_TRACKED_PLANTS,
        "plants": []
    }

    for i in range(NUM_TRACKED_PLANTS):
        plant_data = {
            "wet_saturation": getattr(channels[i], 'wet_saturation'),
            "dry_saturation": getattr(channels[i], 'dry_saturation')
        }
        config_data["plants"].append(plant_data)

    logger.info('Saving calibration data to the config file.')
    with open(CALIBRATION_FILE, 'w', encoding='UTF-8') as outfile:
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

    soil_moisture_readings = []
    for plant in range(NUM_TRACKED_PLANTS):
        soil_moisture_label = input(
            f"Enter the soil moisture label for Plant {plant + 1}: ")
        soil_moisture_percentage = (
            channels[plant].value - channels[plant].wet_saturation) / (
            channels[plant].dry_saturation - channels[plant].wet_saturation) * 100
        soil_moisture_readings.append(
            (soil_moisture_label, soil_moisture_percentage))

    with open(filename, "a", newline='', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)

        header = ["Timestamp"]
        for plant in range(NUM_TRACKED_PLANTS):
            header.append(
                f"Soil Moisture ({soil_moisture_readings[plant][0]})")
        header.extend(["Temperature", "Humidity"])

        values = [timestamp]
        for plant in range(NUM_TRACKED_PLANTS):
            values.append(soil_moisture_readings[plant][1])
        values.extend([bme280.temperature, bme280.relative_humidity])

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
