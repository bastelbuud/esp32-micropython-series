#get data from GY511 and build a tilt gadget
from machine import Pin, SoftI2C
import time
import math
from MPU6050 import MPU6050
import ssd1306




i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
mpu = MPU6050()
dsp = ssd1306.SSD1306_I2C(128, 64, i2c)

pitchComp = 0
rollComp = 0
tLoop = 0
cnt = 0
errorP = 0
errorR = 0

def circle(radius,xOff,yOff):
    xCenter=64
    yCenter=45
    for deg in range(0,360):
        rads=deg/360*2*math.pi
        x=radius*math.cos(rads)
        y=radius*math.sin(rads)
        dsp.pixel(int(x+xCenter-xOff),int(y+yCenter-yOff),1)
 

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
    # basic pitch and roll
    if zAccel == 0:
        zAccel = 0.001
    pitchA=math.atan(yAccel/zAccel)/(2*math.pi)*360
    rollA=math.atan(xAccel/zAccel)/(2*math.pi)*360
    # filter and compensate
    pitchComp=pitchA*.1 + .9*(pitchComp+xGyro*tLoop) + errorP * 0.002
    rollComp=rollA*.1 + .9*(rollComp+yGyro*tLoop) + errorR * 0.002
    
    errorP = errorP + (pitchA-pitchComp)*tLoop
    errorR = errorR + (rollA - rollComp)*tLoop
    
    cnt = cnt+1
    if cnt==100:
        cnt = 0

        print('PA: ',pitchA, 'RA: ',rollA,'PC: ',pitchComp, 'RC: ',rollComp)
        dsp.text('Tiltgadget',0,0)
        msg='P: '+str(round(pitchComp,1))+' R: '+str(round(rollComp,1))
        dsp.text(msg,0,16)
        dsp.rect(0,26,128,38,1)
        dsp.hline(0,45,128,1)
        dsp.vline(64,26,38,1)
        circle(7,int(2.5*pitchComp),int(rollComp))
        dsp.show()
        dsp.fill(0)
    tStop = time.ticks_ms()
    tLoop = (tStop-tStart) * 0.001
          
 



    