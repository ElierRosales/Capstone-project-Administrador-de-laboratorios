import paho.mqtt.client as mqtt #manejo de conexiones mqtt
def on_connect(client, userdata, flags, rc):
	print(f"Conectado con codigo:{rc}")
uid = 2183036000
json = '{"_id":'+str(uid)+'}'
client = mqtt.Client()
client.on_connect = on_connect
client.connect("192.168.1.78", 1883, 60)
client.publish("isur/uid",payload=json,qos=0,retain=False)
