# get data from DHT and display them on display
# DHT 11 data connected to pin 14
# the data is also send to mqtt via wifi to a message broker in order to be used in a smarthome system

from machine import Pin, SoftI2C, reset
from time import sleep
from umqtt.simple import MQTTClient
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import dht
import secrets



I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

# network configuration
def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(secrets.WIFIName, secrets.WIFIPassword)
        while not sta_if.isconnected():
            pass # wait till connection
    print('network config:', sta_if.ifconfig())
    
def mqtt_connect():
    client = MQTTClient(secrets.MQTTClient, secrets.MQTTBroker, 1883, secrets.MQTTUser, secrets.MQTTPassword, keepalive = 60)
    client.connect()
    print('Connected to %s MQTT Broker'%(secrets.MQTTBroker))
    return client

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   sleep(2)
   client = mqtt_connect()
   return client
   
print("Trying to connect to WIFI with ",secrets.WIFIName," and ",secrets.WIFIPassword,)    
connect()
sleep(2)
# mqtt configuration
mqttTopic = "DUMSHOME/DHT11"
print("trying to connect to mqtt")

try:
    mqttc = mqtt_connect()
except OSError as e:
    mqttc = reconnect()

print("connected")
Temp_TOPIC = mqttTopic.encode() + b'/Temp'
Hum_TOPIC = mqttTopic.encode() + b'/Hum'


d = dht.DHT11(Pin(14))
sleep(1)
d.measure()
lcd.putstr("Display Temperature")
sleep(2)
lcd.clear()
while True:
    d.measure()
    t = d.temperature()
    h = d.humidity()
    lcd.move_to(0,0)
    lcd.putstr("Temp: " + str(t))
    lcd.move_to(0,1)
    lcd.putstr("Hum: " + str(h))
    mqttc.publish( Temp_TOPIC, str(t).encode())
    mqttc.publish( Hum_TOPIC, str(h).encode())
    sleep(2)
    lcd.clear()
