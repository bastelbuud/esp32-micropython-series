#get data from GY511 and display them on display
from machine import Pin, SoftI2C
from time import sleep
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from MPU6050 import MPU6050



I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
mpu = MPU6050()
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

lcd.putstr("Display Acc. data")
sleep(2)
lcd.clear()
while True:
    accel = mpu.read_accel_data() # read the accelerometer [ms^-2]
    aX = accel["x"]
    raX = round(aX, 2)
    aY = accel["y"]
    raY = round(aY, 2)    
    aZ = accel["z"]
    raZ = round(aZ, 2)
    # Gyroscope Data
    gyro = mpu.read_gyro_data()   # read the gyro [deg/s]
    gX = gyro["x"]
    rgX = round(gX, 2)   
    gY = gyro["y"]
    rgY = round(gY, 2)
    gZ = gyro["z"]
    rgZ = round(gZ, 2)
    # G-Force
    gforce = mpu.read_accel_abs(g=True) # read the absolute acceleration magnitude
    lcd.move_to(0,0)
    lcd.putstr("Accel: " + str(raX) + " " + str(raY) + " " + str(raZ))
    sleep(2)
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Gyro: " + str(rgX) + " " + str(rgY) + " " + str(rgZ))
    sleep(2)
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("G-Force: " + str(gforce))
    sleep(2)
    lcd.clear()