"""Soil Moisture Sensors"""
import time
import datetime
import json
import csv
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

MAX_VAL = [None, None, None]
MIN_VAL = [None, None, None]

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended inputs for three sensors (channels 0, 1, and 2)
channels = [AnalogIn(ads, ADS.P0), AnalogIn(
    ads, ADS.P1), AnalogIn(ads, ADS.P2)]


# Load calibration data from the JSON file if it exists
CALIBRATION_FILE = 'cap_config.json'

try:
    with open(CALIBRATION_FILE, 'r', encoding='UTF-8') as file:
        calibration_data = json.load(file)

    for i, sensor_data in enumerate(calibration_data.values()):
        MIN_VAL[i] = sensor_data['full_saturation']
        MAX_VAL[i] = sensor_data['zero_saturation']

    print('Calibration data loaded from JSON.')
    print(calibration_data)

except FileNotFoundError:
    print('Calibration file not found. Starting calibration process...')
    # Calibration for each sensor
    for i, chan in enumerate(channels):
        baseline_check = input(
            f"Is Capacitive Sensor {i} Dry? (enter 'y' to proceed): ")
        if baseline_check.lower() == 'y':
            MAX_VAL[i] = chan.value
            print(f"------{'raw':>5}\t{'v':>5}")
        for x in range(0, 10):
            if chan.value > MAX_VAL[i]:
                print(f"CHAN {i}: {chan.value:>5}\t{chan.voltage:>5.3f}")
                time.sleep(0.5)
                print('\n')

        water_check = input(
            f"Is Capacitive Sensor {i} in Water? (enter 'y' to proceed): ")
        if water_check.lower() == 'y':
            MIN_VAL[i] = chan.value
            print(f"------{'raw':>5}\t{'v':>5}")
        for x in range(0, 10):
            if chan.value < MIN_VAL[i]:
                MIN_VAL[i] = chan.value
                print(f"CHAN {i}: {chan.value:>5}\t{chan.voltage:>5.3f}")
                time.sleep(0.5)

    # Create a dictionary with calibration data for all three sensors
    config_data = {}
    for i in range(len(channels)):
        config_data[f"Sensor {i+1}"] = {"full_saturation": MIN_VAL[i],
                                        "zero_saturation": MAX_VAL[i]}

    # Save calibration data to a JSON file
    with open('cap_config.json', 'w', encoding='UTF-8') as outfile:
        json.dump(config_data, outfile)
        print('\n')
        print(config_data)
        time.sleep(0.5)

# Continuous reading and writing of moisture values
today = datetime.date.today().strftime("%d-%m-%y")
filename = f"../data/soil_moistures_{today}.csv"
SAMPLING_INTERVAL = 5  # Interval between readings in seconds

while True:
    try:
        timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())

        with open(filename, "a", newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)

            values = [timestamp]
            for i, chan in enumerate(channels):
                values.extend([chan.value, chan.voltage])

            writer.writerow(values)

        print(f"Moisture values written to {filename} at {timestamp}.")
        time.sleep(SAMPLING_INTERVAL)

    except Exception as error:
        raise error

    except KeyboardInterrupt:
        print('Exiting script.')
        break
