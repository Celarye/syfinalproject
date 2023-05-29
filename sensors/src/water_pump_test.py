"""Water Pump Test Script"""
import time
from gpiozero import OutputDevice

relay_pin = OutputDevice(22)

try:
    relay_pin.on()
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    relay_pin.off()

finally:
    relay_pin.close()
