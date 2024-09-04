#pwm test
import machine
import time
p32 = machine.Pin(32)
pwm32 = machine.PWM(p32)
pwm32.freq(5000)
pwm32.duty(255)
print(pwm32)
while True:
    for i in range(1023):
        pwm32.duty(i)
        print(i)
        time.sleep_ms(10)
    time.sleep(1)    
    for i in range(1023,0,-1):
        pwm32.duty(i)
        print(i)
        time.sleep_ms(10)
    time.sleep(1)
    
