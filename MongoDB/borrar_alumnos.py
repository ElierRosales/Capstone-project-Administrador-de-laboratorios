import pymongo
import time
miCliente = pymongo.MongoClient("mongodb://localhost:27017/")
base_datos = miCliente["UAM"]
alumnos = base_datos["alumnos"]
admin = base_datos["administrativos"]
borrar = alumnos.delete_many({})
borrar_admin = admin.delete_many({})
print(borrar.deleted_count," Alumnos borrados")
print(borrar_admin.deleted_count," Administrativos borrados")
