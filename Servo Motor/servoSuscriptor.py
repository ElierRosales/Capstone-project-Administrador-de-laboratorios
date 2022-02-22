#Autor: Juan Elier Rosales Rosas
#Fecha: 11/02/22
#Descripción: Programa para mover un servomotor simulando la apertura de una puerta
###################################
#Declaración de modulos
###################################
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
###################################
#Configuración de GPIO
###################################
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT) #Se configura el pin 12 como salida
servo = GPIO.PWM(11, 50) # 12 es el pin y 50 el pulso en Hz
###################################
#Configuración cliente MQTT
###################################
def on_connect(client, userdata, flags, rc):
    print("Esperando... ")
   
    client.subscribe("isur/puerta")
    
def on_message(client, userdata, msg):
    abierto=msg.payload.decode()
    acceso(abierto)
###################################
#Función main
###################################   
def main():
    client = mqtt.Client()
    client.connect("187.200.112.52", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message 
    client.loop_forever()
    servo.stop()
    GPIO.cleanup()
    client.disconnect()
    
def acceso(abierto):
    servo.start(0)
    if abierto=='true':
        print("Puerta abierta")
        servo.ChangeDutyCycle(7)
        time.sleep(0.5)
        servo.ChangeDutyCycle(0)
    if abierto=='false':
        print("Puerta cerrada")
        servo.ChangeDutyCycle(2)
        time.sleep(0.5)
        servo.ChangeDutyCycle(0)
        
if __name__ == '__main__':
    main()
