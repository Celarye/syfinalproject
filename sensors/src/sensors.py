"""Sensors"""
import time
import datetime
import json
import csv
import board
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_ccs811

# Create the I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# Create the ADC object using the I2C bus
try:
    ads = ADS.ADS1015(i2c)
except Exception as e:
    print(f"ADS1015 initialization error: {e}")

# Create the BME280 and the CCS811 sensor objects
try:
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
except Exception as e:
    print(f"BME280 initialization error: {e}")

try:
    ccs811 = adafruit_ccs811.CCS811(i2c, address=0x5B)
except Exception as e:
    print(f"CCS811 initialization error: {e}")

# Create single-ended inputs for three sensors (channels 0, 1, and 2)
channels = [AnalogIn(ads, ADS.P0), AnalogIn(
    ads, ADS.P1), AnalogIn(ads, ADS.P2)]


MAX_VAL = [None, None, None]
MIN_VAL = [None, None, None]
bme280.sea_level_pressure = 1013.25  # Lochristi's pressure (hPa) at sea level

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
filename = f"../data/sensorData_{today}.csv"
SAMPLING_INTERVAL = 5  # Interval between readings in seconds

while True:
    try:
        TIMESTAMP = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())

        with open(filename, "a", newline='', encoding='UTF-8') as csvfile:
            WRITER = csv.writer(csvfile)

            header = ["Timestamp"]
            for i, chan in enumerate(channels):
                header.extend([f"Sensor {i+1} Value", f"Sensor {i+1} Voltage"])
            header.extend(["Temperature", "Humidity", "Pressure",
                          "Altitude", "CO2", "TVOC", "Temp"])

            values = [TIMESTAMP]
            for i, chan in enumerate(channels):
                values.extend([chan.value, chan.voltage])
            values.extend([bme280.temperature, bme280.relative_humidity, bme280.pressure,
                          bme280.altitude, ccs811.eco2, ccs811.tvoc, ccs811.temperature])

            # Check if the file is empty (no header present)
            is_empty = csvfile.tell() == 0
            if is_empty:
                WRITER.writerow(header)
            WRITER.writerow(values)

        print(f"Sensor values written to {filename} at {TIMESTAMP}.")
        time.sleep(SAMPLING_INTERVAL)

    except Exception as error:
        raise error

    except KeyboardInterrupt:
        print('Exiting script.')
        break
