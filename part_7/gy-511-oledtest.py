# ssd1306 oled display test
from machine import Pin, SoftI2C
import ssd1306

# using default address 0x3C
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)

display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.text('Hello, World!', 0, 0, 1)
display.show()