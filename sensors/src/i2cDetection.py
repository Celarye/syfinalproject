import board

i2c = board.I2C()

while not i2c.try_lock():
    pass

devices = i2c.scan()

if devices:
    print("I2C devices found:", [hex(device_address) for device_address in devices])
else:
    print("No I2C devices found")
i2c.unlock()
