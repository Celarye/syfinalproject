"""Sensors Script"""
import os
import time
import datetime
import json
import csv
import logging
from threading import Thread
import board
from flask import Flask
from flask_cors import CORS
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_bme280 import basic as adafruit_bme280
from gpiozero import OutputDevice

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Initialize I2C bus and sensors
i2c = board.I2C()
ads = ADS.ADS1015(i2c)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
logger.info("BME280 connected.")
channels = [AnalogIn(ads, ADS.P0), AnalogIn(
    ads, ADS.P1), AnalogIn(ads, ADS.P2)]
sensor_labels = ["Plant 1", "Plant 2", "Plant 3"]
logger.info("Soil moisture sensors connected.")
relay_pin = OutputDevice(22)
logger.info("Water pump for plant 1 connected.")

# Set up Flask app
app = Flask(__name__)
CORS(app)

# Define calibration file and soil moisture sensors values
CALIBRATION_FILE = 'config.json'
DRY_SATURATION = [None, None, None]
WET_SATURATION = [None, None, None]

# Load soil moisture sensors calibration data from config file if available
try:
    with open(CALIBRATION_FILE, 'r', encoding='UTF-8') as file:
        calibration_data = json.load(file)

    sensors_data = calibration_data.get('sensors')

    if sensors_data:
        for i, sensor_data in enumerate(sensors_data):
            WET_SATURATION[i] = sensor_data.get('wet_saturation')
            DRY_SATURATION[i] = sensor_data.get('dry_saturation')

        logger.info(
            'Soil moisture sensors calibration data loaded from the config file.')
        logger.info(calibration_data)

# If calibration file not found, initiate calibration process
except FileNotFoundError:
    logger.info(
        "Calibration file not found. Initiating soil moisture sensors calibration process...")

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

    logger.info(
        'Saving soil moisture sensors calibration data to the config file.')

    with open('config.json', 'w', encoding='UTF-8') as outfile:
        json.dump(config_data, outfile)
        logger.info(config_data)

# Load Raspberry Pi IP address and soil moisture threshold from config file
RASPBERRY_PI_IP_ADDRESS = None
SOIL_MOISTURE_THRESHOLD_VALUE_PLANT_1 = None

with open(CALIBRATION_FILE, 'r', encoding='UTF-8') as file:
    calibration_data = json.load(file)

RASPBERRY_PI_IP_ADDRESS = calibration_data.get('raspberry_pi_ip_address')
SOIL_MOISTURE_THRESHOLD_VALUE_PLANT_1 = calibration_data.get(
    'soil_moisture_threshold_value_plant_1')

# If IP address or threshold value is missing, initiate calibration process
if not RASPBERRY_PI_IP_ADDRESS or not SOIL_MOISTURE_THRESHOLD_VALUE_PLANT_1:
    logger.info(
        "The Raspberry Pi its IP address and the soil moisture threshold value for Plant 1\
              are missing from the config file. Initiating calibration process...")
    RASPBERRY_PI_IP_ADDRESS = input(
        'Please enter the Raspberry Pi its IP address: ')
    threshold_input = input(
        'Please enter the soil moisture threshold value for plant 1 (in percentage): ')

    try:
        SOIL_MOISTURE_THRESHOLD_VALUE_PLANT_1 = int(
            threshold_input.rstrip('%'))
    except ValueError:
        logger.error("Invalid threshold value. Please try again.")
        exit()

    calibration_data['raspberry_pi_ip_address'] = RASPBERRY_PI_IP_ADDRESS
    calibration_data['soil_moisture_threshold_value_plant_1'] = \
        SOIL_MOISTURE_THRESHOLD_VALUE_PLANT_1

    logger.info(
        'Saving the Raspberry Pi its IP address and the soil moisture threshold value for plant 1\
              to the config file.')

    with open(CALIBRATION_FILE, 'w', encoding='UTF-8') as file:
        json.dump(calibration_data, file)
        logger.info(calibration_data)

# Start Flask app
logger.info("Starting Flask app...")

values = ["Timestamp"] + [f"Soil Moisture ({label})" for label in sensor_labels] + [
    "Temperature", "Air Humidity", "Plant 1 Watering"]

WATERING_OCCURRED = False
last_watering_time = None


@app.route('/')
def index():
    """Flask index"""
    return str(values)


# Start Flask app in a separate thread
flask_thread = Thread(target=app.run, kwargs={
    'host': RASPBERRY_PI_IP_ADDRESS, 'port': 5000})
flask_thread.start()

# Start sensors data monitoring, response, and logging
logger.info("Starting sensors data monitoring, response and logging...")

RUNNING = True
while RUNNING:
    try:
        today = datetime.date.today().strftime("%d-%m-%Y")
        DIRECTORY = "../data/"
        filename = f"{DIRECTORY}sensorsData_{today}.csv"

        os.makedirs(DIRECTORY, exist_ok=True)

        timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        SAMPLING_INTERVAL = 60

        sensor_readings = []
        for i, channel in enumerate(channels):
            soil_moisture_percentage = (
                channel.value - DRY_SATURATION[i]) / (WET_SATURATION[i] - DRY_SATURATION[i]) * 100
            sensor_readings.append(soil_moisture_percentage)

        with open(filename, "a", newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)

            header = ["Timestamp"] + [f"Soil Moisture ({label})" for label in sensor_labels] + [
                "Temperature", "Humidity", "Plant 1 Watering"]

            if not WATERING_OCCURRED:
                PLANT_1_WATERING = "Not watered yet"
            else:
                PLANT_1_WATERING = last_watering_time

            values = [timestamp] + sensor_readings + \
                [bme280.temperature, bme280.relative_humidity, PLANT_1_WATERING]

            plant1_reading = sensor_readings[0]

            if plant1_reading < SOIL_MOISTURE_THRESHOLD_VALUE_PLANT_1:
                current_time = datetime.datetime.now()
                time_since_last_watering = current_time - last_watering_time
                if time_since_last_watering.total_seconds() >= 1800:
                    logger.info(
                        "Soil moisture level for Plant 1 has dropped below the set threshold.\
                            Starting the watering process...")
                    relay_pin.on()
                    last_watering_time = current_time
                    time.sleep(5)
                    relay_pin.off()
                    values[-1] = last_watering_time
                    WATERING_OCCURRED = True
                    logger.info("Successfully watered Plant 1 at %s",
                                last_watering_time)
                else:
                    logger.info(
                        "Skipping watering for Plant 1.\
                            Minimum time interval since last watering not met.")
            else:
                logger.info(
                    "Soil moisture level for Plant 1 is above the set threshold.\
                          No watering needed.")

            is_empty = csvfile.tell() == 0
            if is_empty:
                writer.writerow(header)
            writer.writerow(values)

        logger.info("Sensors values and response data written to %s at %s.",
                    filename, timestamp)
        logger.info("Flask app data has been updated (http://%s:5000/).",
                    RASPBERRY_PI_IP_ADDRESS)
        logger.info("Sensors values and response data: %s", values)

        time.sleep(SAMPLING_INTERVAL)

    except IOError:
        logger.error(
            "An error occurred while logging the sensors data.", exc_info=True)

    except KeyboardInterrupt:
        logger.info(
            "Exiting sensor data monitoring, response, logging and terminating the Flask app.")
        relay_pin.close()
        RUNNING = False

flask_thread.join()
