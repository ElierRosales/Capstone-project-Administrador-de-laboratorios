"""
Administrador de base de datos: Registro UAM-LERMA
Autor: Jorge Isur Balderas Ramirez
Fecha: 13-12-2021
"""
import pymongo
import time
import paho.mqtt.client as mqtt #manejo de conexiones mqtt
import json
import datetime as dt
miCliente = pymongo.MongoClient("mongodb://localhost:27017/")
base_datos = miCliente["UAM"]
alumnos = base_datos["alumnos"]
admin = base_datos["administrativos"]
def on_connect(client,userdata,flags,rc):
   print(f"Conectado con codigo:{rc}")
   client.subscribe("isur/uid")
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
   menu(uid,fecha)
def existeDatabase(db):
    dblist = miCliente.list_database_names()
    if db in dblist:
        print(f"Base de datos {db} encontrada.\n")
        return True
    else:
        print(f"Base de datos {db} no existente.\n")
        return False
        exit()
def existeCollecion(coleccion):
    listaColeccion = base_datos.list_collection_names()
    if coleccion in listaColeccion:
        print(f"Colección {coleccion} encontrada.\n")
        return True
    else:
        print(f"Collecion {coleccion} no existente.\n")
        print("No hay usuarios registrados.")
        return False
        exit()
def registro(uid,fecha):
    print("***********************************************")
    print("*******************REGISTRO********************")
    opcion=input("Ingrese 0 para regresar al menú y 1 para continuar.\n")
    if opcion=='0':
        menu()
    tipo = input("1. Profesor/Administrativo\n"
                 "2. Alumno\n")
    nombre = input("Ingresa el nombre:\t")
    matricula = input("Ingresa la matricula:\t")           
    info = input("Ingresa la carrera:\t") 
    miRegistro = {"_id":uid,"nombre":nombre,"info":info,"matricula":matricula,"fecha_entrada":fecha,"fecha_salida":"/-/-/-/"}
    if tipo=='1':
        for dato in admin.find({},{"_id":1}):
            if dato["_id"]==matricula:
                print("Esta matricula ya fue registrada con anterioridad")
                exit()
        push = admin.insert_one(miRegistro)
        print("*************************************************")
        print("Registro exitoso.\n")
        print("*************************************************")
        time.sleep(2)
        ordenamiento = admin.find().sort("nombre",-1)
    if tipo=='2':
        for dato in alumnos.find({},{"_id":1}):
            if dato["_id"]==matricula:
                print("Esta matricula ya fue registrada con anterioridad")
                exit()
        push = alumnos.insert_one(miRegistro)
        print("*************************************************")
        print("Registro exitoso.\n")
        print("*************************************************")
        ordenamiento = alumnos.find().sort("nombre",-1)
def menu(uid,fecha):
   print("""-------------------MENU---------------------
   1-Registro
   2-Mostrar todos los alumnos
   3-Mostrar todos los administrativos/profesores
   --------------------------------------------""")
   opcion = input("Ingresa tu opcion--->")
   if opcion == '1':
      registro(uid,fecha)
   if opcion == '2':
      print("****************************************")
      print("*****************ALUMNOS****************")
      estado_db = existeDatabase("UAM")
      estado_col = existeCollecion("alumnos")
      if estado_db and estado_col:
         for datos in alumnos.find():
            print("****************************************")
            print("Nombre:\t"+datos["nombre"])
            print("UID:\t"+uid)
            print("Carrera:\t"+datos["info"])
            print("Matricula:\t"+datos["matricula"])
            print("Ultima entrada:\t"+str(datos["fecha_entrada"]))
            print(f"Ultima salida:{datos['fecha_salida']}")
            print("****************************************")
   if opcion == '3':
      print("****************************************")
      print("*****************ADMIN******************")
      estado_db2 = existeDatabase("UAM")
      estado_col2 = existeCollecion("administrativos")
      if estado_db2 and estado_col2:
         for datos in admin.find():
            print("****************************************")
            print("Nombre:\t"+datos["nombre"])
            print("UID:\t"+uid)
            print("Carrera:\t"+datos["info"])
            print("Matricula:\t"+datos["matricula"])
            print(f'Ultima entrada: {datos["fecha"]}')
            print("****************************************")
try:
    client = mqtt.Client("Isur-PC")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.1.72", 1883, 60)
    print("Acerca la tarjeta al lector.")
    client.loop_forever()
except KeyboardInterrupt:
    print("\n")
    print("Finalizando programa.")