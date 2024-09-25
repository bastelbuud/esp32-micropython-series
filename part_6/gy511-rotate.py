#get data from GY511 and display them on display
from machine import Pin, SoftI2C
import time
import math
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
time.sleep(2)
lcd.clear()
roll = 0
pitch = 0
yaw = 0
rollA = 0
rollComp = 0
pitchComp = 0
pitchA = 0
yawA = 0
cnt = 0
tLoop = 0
while True:
    tStart=time.ticks_ms()
    gyro = mpu.read_gyro_data()
    accel = mpu.read_accel_data()
    xGyro = gyro["x"]
    yGyro = -gyro["y"]
    zGyro = gyro["z"]
    xAccel = accel["x"]
    yAccel = accel["y"]
    zAccel = accel["z"]
    
    roll = roll + yGyro*tLoop
    pitch = pitch + xGyro*tLoop
    yaw = yaw + zGyro*tLoop
    
    rollA = math.atan(xAccel/zAccel)/2/math.pi*360
    pitchA = math.atan(yAccel/zAccel)/2/math.pi*360
    rollComp = rollA *0.1 + 0.9 *(rollComp + yGyro*tLoop)
    pitchComp = pitchA *0.1 + 0.9 *(pitchComp + xGyro*tLoop) 
    cnt = cnt + 1
    if cnt == 10:
        cnt = 0
        print("rollC: ",rollComp,"pC: ", pitchComp,)
    tStop = time.ticks_ms()
    tLoop = (tStop-tStart) * 0.001
    