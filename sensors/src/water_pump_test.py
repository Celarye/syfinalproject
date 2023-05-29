"""Water Pump Test Script"""
import time
from gpiozero import OutputDevice

relay_pin = OutputDevice(22)

try:
    relay_pin.on()
    time.sleep(5)
    relay_pin.off()

except KeyboardInterrupt:
    relay_pin.close()
