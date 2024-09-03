from machine import Pin
from time import sleep, sleep_ms 
led = Pin(32,Pin.OUT)
while True:
    led.value(True)
    sleep(1)
    led.value(False)
    sleep(1)
    