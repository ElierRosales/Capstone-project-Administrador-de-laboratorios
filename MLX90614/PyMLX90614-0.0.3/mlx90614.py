#declaracion de modulos
from smbus2 import SMBus #administrar el bus de datos
import paho.mqtt.client as mqtt #manejo de conexiones mqtt
from mlx90614 import MLX90614 #manejo del sensor de temperatura
import time #manejo del tiempo
import RPi.GPIO as gpio #control del acceso GPIO de la raspberry
import random #generacion de numeros aleatorios
import urllib.request as urllib2 #comprobacion de conexion a internet
import datetime as dt
#instancias de objetos
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
#LEDS Y PINES
LED_ENCENDIDO = 12
LED_MQTT = 16
LED_LECTURA = 18
pin_button = 22
#funcion para conectarnos a mqtt
def on_connect(client, userdata, flags, rc):
    for i in range(2):
        gpio.output(LED_MQTT,True)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_MQTT,False)
    print(f"Conectado con codigo de resultado {rc}")
def hayInternet():
    try:
        urllib2.urlopen('http://google.com.mx', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False
def standby(LED_ENCENDIDO,LED_MQTT,LED_STANDBY):
    modo = random.randint(0,3)
    if modo == 0:
        gpio.output(LED_ENCENDIDO,False)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_LECTURA,True)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,False)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_LECTURA,True)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_LECTURA,True)
        time.sleep(1)
    if modo ==1:
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_LECTURA,False)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_LECTURA,False)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_LECTURA,True)
        time.sleep(1)
    if modo ==2:
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_LECTURA,True)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,False)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_LECTURA,False)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_LECTURA,True)
        time.sleep(1)
    if modo ==3:
        gpio.output(LED_ENCENDIDO,False)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_LECTURA,True)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,False)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_LECTURA,True)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_LECTURA,False)
        time.sleep(1)
def parpadeo(LED):
    gpio.output(LED,True)
    gpio.output(LED,False)
    gpio.output(LED,False)
    time.sleep(1)
def mostrarHora():
    hora = dt.datetime.now().hour
    minutos = dt.datetime.now().minute
    dia = dt.datetime.now().day
    mes = dt.datetime.now().month
    year = dt.datetime.now().year
    if minutos<10:
        minutos = '0'+str(minutos)
    print(f"{dia}/{mes}/{year} a las {hora}:{minutos}")
#programa principal
try:
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(pin_button,gpio.IN,pull_up_down=gpio.PUD_DOWN)
    gpio.setup(LED_ENCENDIDO,gpio.OUT)
    gpio.setup(LED_MQTT,gpio.OUT)
    gpio.setup(LED_LECTURA,gpio.OUT)
    while(hayInternet()==False):
        print("No se encuentra una conexion a Internet.")
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_ENCENDIDO,False)
        print("Reintentando en 5 segundos...")
        time.sleep(5)
    print("Conectado a Internet.")
    gpio.output(LED_ENCENDIDO,True)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("192.168.1.78", 1883, 60)
    while(1):
        if(gpio.input(pin_button)==gpio.HIGH):
            print("Iniciando lectura:\n")
            parpadeo(LED_LECTURA)
            print("Temperatura ambiente:"+str(sensor.get_ambient()))
            parpadeo(LED_LECTURA)
            print("temperatura objeto:"+str(sensor.get_object_1()))
            parpadeo(LED_LECTURA)
            client.publish('isur/temperatura_salon', payload = sensor.get_ambient(),qos=0,retain=False)
            parpadeo(LED_MQTT)
            client.publish('isur/temp',payload = sensor.get_object_1(),qos=0,retain=False)
            parpadeo(LED_MQTT)
            time.sleep(5)
        else:
            mostrarHora()
            print("Presione el boton durante 3 segundos para iniciar la lectura.")
            standby(LED_ENCENDIDO,LED_MQTT,LED_LECTURA)
except KeyboardInterrupt:
    print("Finalizando programa.")
    print(f"Apagando leds GPIO{LED_MQTT},GPIO{LED_ENCENDIDO},GPIO{LED_LECTURA}")
    gpio.output(LED_ENCENDIDO,False)
    gpio.output(LED_MQTT,False)
    gpio.output(LED_LECTURA,False)
    bus.close()
