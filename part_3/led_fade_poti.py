#pwm test
import machine
import time

#led config
p32 = machine.Pin(32)
pwm32 = machine.PWM(p32)
pwm32.freq(5000)
pwm32.duty(255)

#poti config
pot = machine.ADC(machine.Pin(33))
pot.width(machine.ADC.WIDTH_10BIT)
pot.atten(machine.ADC.ATTN_11DB)

                  
while True:
    pot_value = pot.read()
    pwm32.duty(pot_value)
    time.sleep(0.1)    

    
