"""
Administrador de base de busqueda: Busqueda UAM-LERMA
Autor: Jorge Isur Balderas Ramirez
Fecha: 03-02-2021
"""
import pymongo
import time
import paho.mqtt.client as mqtt #manejo de conexiones mqtt
import json
import datetime as dt
import os

miCliente = pymongo.MongoClient("mongodb://localhost:27017/")
base_datos = miCliente["UAM"]
alumnos = base_datos["alumnos"]
admin = base_datos["administrativos"]

global broker_ip
global port
global cliente
broker_ip = "192.168.1.72"
port = 1883
cliente = 'Isur-PC'
global separador
separador ="**************************************"

def on_connect(client,userdata,flags,rc):
   print(f"Cliente:{cliente}")
   if rc==0:
        print("Conexión exitosa")
        client.subscribe("isur/uid")
   else:
       print(f"Conexion con {broker_ip}:{port} fallida, codigo de error: {rc}")
def on_message(client,userdata,msg):
   uid = msg.payload
   uid = uid.decode()
   print(f"Tarjeta detectada con UID:{uid}")
   fecha  = dt.datetime.now()
   hora = dt.datetime.now().hour
   minuto = dt.datetime.now().minute
   dia = dt.datetime.now().day
   mes = dt.datetime.now().month
   if hora < 10:
       hora = '0'+str(hora)
   if minuto <10:
       minuto = '0'+str(minuto)
   if mes < 10:
       mes = '0'+str(mes)
   if dia < 10:
       dia = '0'+str(dia)
   print(f"Fecha:{dia}-{mes}-{fecha.year} {hora}:{minuto}")
   client.unsubscribe("isur/uid")
   client.disconnect()
   existe = busqueda(uid,fecha)
   if existe ==False:
       print("Usuario no existente.")
       os.system("python buscarUID.py")
   else:
       print("Usuario encontrado.")
       print("Datos enviados")
def existeDatabase(db):
    dblist = miCliente.list_database_names()
    if db in dblist:
        print(f"Base de busqueda {db} encontrada.\n")
        return True
    else:
        print(f"Base de busqueda {db} no existente.\n")
        return False
        exit()
def existeCollecion(coleccion):
    listaColeccion = base_datos.list_collection_names()
    if coleccion in listaColeccion:
        print(f"Colección {coleccion} encontrada.\n")
        return True
    else:
        print(f"Collecion {db} no existente.\n")
        return False
        exit()
def busqueda(uid,fecha):
    existe = False
    print(separador)
    busqueda = alumnos.find_one(uid)
    if busqueda !=None:
        nombre =busqueda["nombre"]
        print(f"Nombre:{nombre}")
        _id = busqueda["_id"]
        print(f"UID:{_id}")
        carrera = busqueda["info"]
        print(f"Carrera:{carrera}")
        matricula  = busqueda["matricula"]
        print(f"Matricula:{matricula}")
        fecha_entrada = busqueda["fecha_entrada"]
        print(f"Ultima entrada registrada:{fecha_entrada}")
        client.publish("isur/ultima_entrada",payload=str(fecha_entrada),qos=0,retain=False)
        fecha_salida = busqueda["fecha_salida"]
        print(f"Ultima salida registrada: {fecha_salida}")
        client.publish("isur/ultima_salida",payload=str(fecha_salida),qos=0,retain=False)
        estado = entradaSalida(fecha,fecha_entrada,fecha_salida)
        if estado==True:
            query = {"nombre":nombre}
            nuevaFecha = {"$set":{"fecha_entrada":fecha}}
            actualizar=alumnos.update_one(query,nuevaFecha)
            print(f"{actualizar.modified_count} registros actualizados")
        if estado==False:
            query = {"nombre":nombre}
            nuevaFecha = {"$set":{"fecha_salida":fecha}}
            actualizar = alumnos.update_one(query,nuevaFecha)
            print(f"{actualizar.modified_count} registros actualizados")
        print(separador)
        print("publicando...")
        client.connect("192.168.1.72", 1883, 60)
        client.publish("isur/usuario/nombre",payload=nombre,qos=0,retain=False)
        client.publish("isur/usuario/carrera",payload=carrera,qos=0,retain=False)
        client.publish("isur/usuario/matricula",payload=matricula,qos=0,retain=False)
        client.publish("isur/ultima_entrada",payload=str(fecha_entrada),qos=0,retain=False)
        client.publish("isur/ultima_salida",payload=str(fecha_salida),qos=0,retain=False)
        return True
    resultados = admin.find_one(uid)
    if resultados !=None:
        nombre =resultados["nombre"]
        print(f"Nombre:{nombre}")
        _id = resultados["_id"]
        print(f"UID:{_id}")
        carrera = resultados["info"]
        print(f"Carrera:{carrera}")
        matricula  = resultados["matricula"]
        print(f"Matricula:{matricula}")
        fecha_entrada = busqueda["fecha_entrada"]
        print(f"Ultima entrada registrada:{fecha_entrada}")
        fecha_salida = busqueda["fecha_salida"]
        print(f"Ultima salida registrada: {fecha_salida}")
        estado = entradaSalida(fecha,fecha_entrada,fecha_salida)
        if estado==True:
            query = {"nombre":nombre}
            nuevaFecha = {"$set":{"fecha_entrada":fecha}}
            actualizar=admin.update_one(query,nuevaFecha)
            print(f"{actualizar.modified_count} registros actualizados")
        if estado==False:
            query = {"nombre":nombre}
            nuevaFecha = {"$set":{"fecha_salida":fecha}}
            actualizar = admin.update_one(query,nuevaFecha)
            print(f"{actualizar.modified_count} registros actualizados")
        client.connect("192.168.1.78", 1883, 60)
        client.publish("isur/usuario/nombre",payload=nombre,qos=0,retain=False)
        client.publish("isur/usuario/carrera",payload=carrera,qos=0,retain=False)
        client.publish("isur/usuario/matricula",payload=matricula,qos=0,retain=False)
        return True
    return False
def entradaSalida(fecha,fecha_entrada,fecha_salida):
    try:
        if fecha_entrada > fecha_salida:
            print(f"Salio:{fecha}")
            return False
        if fecha > fecha_salida:
            print(f"Entro:{fecha}")
            return True
    except TypeError:
        print("Comparacion no permitida.")
        print(f"Salio:{fecha}")
        return False
print(separador)
print("ACCESO")
print(separador)
try:
    client = mqtt.Client(cliente)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_ip, port, 60)
    print("Acerca la tarjeta al lector.")
    print(f"Conectando a {broker_ip}:{port}")
    client.loop_forever()
except Exception as err:
    print(err)
    print(f"No es posible conectarse al Broker {broker_ip}:{port}")
    print("Revisa tu conexión")
except KeyboardInterrupt:
    print("\n")
    print("Finalizando programa.")