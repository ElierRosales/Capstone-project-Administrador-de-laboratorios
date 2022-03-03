import pymongo
import time
import paho.mqtt.client as mqtt #manejo de conexiones mqtt
import datetime as dt

miCliente = pymongo.MongoClient("mongodb://localhost:27017/")
base_datos = miCliente["Inventario"]
lab_disponibles = base_datos["lab_disponibles"]

global separador
global laboratorio
global err_counter
err_counter = 0
separador = "********************************************"

def registroElemento(laboratorio,laboratorio_nombre):
    print(separador)
    print(f"Registro de elementos en laboratorio {laboratorio_nombre}")
    print(separador)
    nombre_elemento = input("Ingresa el nombre del artículo-->")
    num_inventario = input("Ingresa el número de inventario-->")
    descripcion = input("Ingresa la descripción del artículo-->")
    registro = {"nombre":nombre_elemento,"num_inventario":num_inventario,"descripcion":descripcion,"disponibilidad":"stock"}
    try:
        insertar = laboratorio.insert_one(registro)
    except Exception as e:
        print(separador)
        print("Ocurrió un error al insertar el elemento")
        print(f"Error:{e}")
        print("Intentalo de nuevo.")
        print(separador)
        registroElemento(laboratorio)
        err_counter+=1
        if err_counter>4:
            salir()
    print(separador)
    print("Registro exitoso")
    err_counter=0
    print(separador)
    menu(laboratorio,laboratorio_nombre)
def borrarElemento(laboratorio,laboratorio_nombre):
    print(separador)
    print(f"Borrar elemento en laboratorio {laboratorio_nombre}")
    print(separador)
    num_inventario = input("Ingresa el número de inventario del artículo a borrar--->")
    query = {"num_inventario":num_inventario}
    try:
        borrar = laboratorio.delete_one(query)
    except Exception as e:
        print(separador)
        print("Ocurrió un error al borrar el elemento.")
        print(f"Error:{e}")
        print("Intentalo de nuevo.")
        print(separador)
        err_counter+=1
        if err_counter>4:
            salir()
    print(separador)
    print(f"{borrar.deleted_count} elementos borrados.")
    print("Borrado exitoso.")
    print(separador)
    menu(laboratorio,laboratorio_nombre)
def imprimirDatabase(laboratorio,laboratorio_nombre):
    print(separador)
    print(laboratorio_nombre)
    print(separador)
    for data in laboratorio.find():
        print(separador)
        print(f"Nombre:{data['nombre']}")
        print(f"Número de inventario:{data['num_inventario']}")
        print(f"Descripción:{data['descripcion']}")
        print(separador)
    menu(laboratorio,laboratorio_nombre)
def existeDatabase(db):
    dblist=miCliente.list_database_names()
    if db in dblist:
        print(f"Base de datos {db} encontrada.\n")
        return True
    else:
        print(f"Base de datos {db} no encontrada.\n")
        return False
def existeColeccion(coleccion):
    listaColeccion = base_datos.list_collection_names()
    if coleccion in listaColeccion:
        print(f"Colección {coleccion} encontrada.\n")
        return True
    else:
        print(f"Colección {coleccion} no existente.\n")
        return False
def menu(laboratorio,laboratorio_nombre):
    print(separador)
    print("MENU")
    print(f"Laboratorio {laboratorio_nombre}")
    print(separador)
    print("""
    1.Registrar nuevo elemento
    2.Borrar elemento existente
    3.Mostrar elementos existentes
    4.Salir
    """)
    eleccion = input("Ingresa la opción--->")
    if eleccion == '1':
        registroElemento(laboratorio,laboratorio_nombre)
    if eleccion == '2':
        borrarElemento(laboratorio,laboratorio_nombre)
    if eleccion == '3':
        imprimirDatabase(laboratorio,laboratorio_nombre)
    if eleccion == '4':
        salir()
def defineLab(laboratorio):
    laboratorio_col = base_datos[laboratorio]
    return laboratorio_col

try:
    print(separador)
    print(f"Sistema de administración de inventario\n")
    print(separador)
    laboratorio_nombre = input("Ingresa el laboratorio a administrar-->").upper()
    laboratorio_col = defineLab(laboratorio_nombre)
    menu(laboratorio_col,laboratorio_nombre)
except KeyboardInterrupt:
    print("\n")
    print("Saliendo...\n")

