import paho.mqtt.client as mqtt
global msgstr
client = mqtt.Client()
#Aquí hay que poner la dirección ip del broker que estemos ocupando
client.connect("187.200.112.52", 1883, 60)
#El valor entre comillas simples es el tema
#ahí se pone tu tema al que quieres mandar el mensaje.
#El siguiente valor entre comillas es el valor para actualizar
#el estado del servo.
client.publish('isur/puerta', "true", qos=1,retain=False)