import paho.mqtt.client as mqtt
import time
import Adafruit_DHT as dht

sensor = dht.DHT11

pin = 23

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.

###################################
#Configuración cliente MQTT
###################################
def on_connect(client, userdata, flags, rc):
    print("Esperando... ")
   
    client.subscribe("isur/humedad")
    
def on_message(client, userdata, msg):
    abierto=msg.payload.decode()
    acceso(abierto)
###################################
#Función main
###################################   
try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("test.mosquitto.org", 1883, 60)
    
    humidity, temperature = dht.read_retry(sensor, pin)
    while (True):
        if humidity is not None and temperature is not None:
            print('Temperatura={0:0.1f}*C  Humedad={1:0.1f}%'.format(temperature, humidity))
            client.publish('isur/temperatura_salon', payload = temperature,qos=0,retain=False)
            client.publish('isur/humedad', payload = humidity,qos=0,retain=False)  
            time.sleep(5)
        else:
            print("Failed to get reading. Try again")
except KeyboardInterrupt:
    print("Terminando programa")