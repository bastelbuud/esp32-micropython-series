from machine import Pin
from time import sleep

led = Pin(32, Pin.OUT)
push_button = Pin(33, Pin.IN)

while True:
    status = push_button.value()
    if status == True:
        led.value(True)
    if status == False:
        led.value(False)
    sleep(1)
    