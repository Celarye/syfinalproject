"""Water Pump Test Script"""
import time
from gpiozero import OutputDevice

relay_pin = OutputDevice(22)

try:
    relay_pin.on()

except KeyboardInterrupt:
    relay_pin.off()
    relay_pin.close()
