# get data from DHT and display them on display
# DHT 11 data connected to pin 14
from machine import Pin, SoftI2C
from time import sleep
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import dht



I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

d = dht.DHT11(Pin(14))
sleep(1)
d.measure()
lcd.putstr("Display Temperature")
sleep(2)
lcd.clear()
while True:
    d.measure()
    lcd.move_to(0,0)
    lcd.putstr("Temp: " + str(d.temperature()))
    lcd.move_to(0,1)
    lcd.putstr("Hum: " + str(d.humidity()))
    sleep(2)
    lcd.clear()