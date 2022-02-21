import pymongo
import time
miCliente = pymongo.MongoClient("mongodb://localhost:27017/")
base_datos = miCliente["UAM"]
alumnos = base_datos["alumnos"]
admin = base_datos["administrativos"]
def registro():
    print("***********************************************")
    print("*******************REGISTRO********************")
    opcion=input("Ingrese 0 para regresar al menú y 1 para continuar.\n")
    if opcion=='0':
        menu()
    tipo = input("1. Profesor/Administrativo\n"
                 "2. Alumno\n")
    nombre = input("Ingresa tu nombre:\t")
    matricula = input("Ingresa tu matricula:\t")           
    info = input("Ingresa tu correo institucional:\t") 
    password = input("Ingresa tu contraseña:\t")
    prueba_pass = input("Vuelve a ingresar tu contraseña:\t")
    if password !=prueba_pass:
        print("Contraseña incorrecta.")
        print("Intenta registrarte de nuevo.")
        time.sleep(2)
        registro()
    miRegistro = {"nombre":nombre,"_id":matricula,"info":info,"password":password}
    if tipo=='1':
        for dato in admin.find({},{"_id":1}):
            if dato["_id"]==matricula:
                print("Esta matricula ya fue registrada con anterioridad")
                registro()
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
                registro()
        push = alumnos.insert_one(miRegistro)
        print("*************************************************")
        print("Registro exitoso.\n")
        print("*************************************************")
        ordenamiento = alumnos.find().sort("nombre",-1)
def login():
    print("***********************************************")
    print("*******************LOGIN********************")
    opcion=input("Ingrese 0 para regresar al menú y 1 para continuar.\n")
    if opcion=='0':
        menu()
    matricula = input("Ingresa tu matricula.\t")
    contra = input("Ingresa tu contraseña\t")
    tipo = input("1. Profesor/Administrativo\n"
                 "2. Alumno\n")
    busqueda = {"_id":matricula,"password":contra}
    if tipo=='1':
        process=admin.find({"_id":matricula},{"password":1})
        for dato in process:
            if dato["password"]==contra:
                print("Validación exitosa.\n")
            else:
                print("Contraseña incorrecta.\n")
    if tipo=='2':
        process=alumnos.find({"_id":matricula},{"password":1})
        for dato in process:
            if dato["password"]==contra:
                print("Validación exitosa.\n")
                time.sleep(2)
            else:
                print("Contraseña incorrecta\n")
                print("Inicio de sesión fallido\n")
                time.sleep(2)
                login()
def existeDatabase(db):
    dblist = miCliente.list_database_names()
    if db in dblist:
        print("Base de datos encontrada.\n")
        return True
    else:
        print("Base de datos no existente.\n")
        return False
        menu()

def existeCollecion(coleccion):
    listaColeccion = base_datos.list_collection_names()
    if coleccion in listaColeccion:
        print("Colección encontrada.\n")
        return True
    else:
        print("Collecion no existente.\n")
        return False
        menu()
def eliminarUsuario(matricula,tipo):
    if tipo=='1':
        seleccion = {"_id":matricula}
        admin.delete_one(seleccion)
    if tipo=='2':
        seleccion = {"_id":matricula}
        alumnos.delete_one(seleccion)
def actualizarDatosUsuario(matricula,tipo):
    if tipo=='1':
        comprobacion = {"_id":matricula}
        existe = admin.find_one(comprobacion)
        if existe!=None:
            pass
        else:
            print("Usuario no encontrado.\n")
            print("Intente de nuevo.\n")
            time.sleep(2)
            menu()
        print("Administrativo seleccionado:\n")
        peticion = {"_id":matricula}
        for datos in admin.find(peticion):
            print("Nombre:\t"+datos["nombre"])
            nombreAdmin = datos["nombre"]
            print("Matricula\t"+datos["_id"])
            matriculaAdmin = datos["_id"]
            print("Correo:\t"+datos["info"])
            infoAdmin = datos["info"]
            print("Contraseña\t"+datos["password"])
            passAdmin = datos["password"]
        print("¿Que datos desea actualizar?")
        print("1.Nombre\n"
          "2.Matricula\n"
          "3.Correo\n"
          "4.Contraseña\n"
          "0.Ninguno\n")
        seleccion = input("=>")
        if seleccion=='1':
            query = {"nombre":nombreAdmin}
            nuevoNombre = input("Ingrese el nuevo nombre:\t")
            nuevoValor = {"$set":{"nombre":nuevoNombre}}
            admin.update_one(query,nuevoValor)
        if seleccion=='2':
            query = {"_id":matriculaAdmin}
            nuevaMatricula = input("Ingresa la nueva matricula:\t")
            nuevoValor = {"$set":{"_id":nuevaMatricula}}
            admin.update_one(query,nuevoValor)
        if seleccion=='3':
            query = {"info":infoAdmin}
            nuevaInfo = input("Ingresa el nuevo correo:\t")
            nuevoValor = {"$set":{"info":nuevaInfo}}
            admin.update_one(query,nuevoValor)
        if seleccion=='4':
            query = {"password":passAdmin}
            nuevaPass = input("Ingresa la nueva contraseña:\t")
            nuevoValor = {"$set",{"password":nuevaPass}}
            admin.update_one(query,nuevoValor)
        if seleccion=='0':
            menu()
    if tipo=='2':
        comprobacion = {"_id":matricula}
        existe = alumnos.find_one(comprobacion)
        if existe!=None:
            pass
        else:
            print("Usuario no encontrado.\n")
            print("Intente de nuevo.\n")
            time.sleep(2)
            menu()
        print("Alumno seleccionado:\n")
        peticion={"_id":matricula}
        for datos in alumnos.find(peticion):
            print("Nombre:\t"+datos["nombre"])
            nombreAlumno = datos["nombre"]
            print("Matricula\t"+datos["_id"])
            matriculaAlumno = datos["_id"]
            print("Correo:\t"+datos["info"])
            infoAlumno = datos["info"]
            print("Contraseña\t"+datos["password"])
            passAlumno = datos["password"]
        print("¿Que datos desea actualizar?")
        print("1.Nombre\n"
          "2.Matricula\n"
          "3.Correo\n"
          "4.Contraseña\n"
          "0.Ninguno\n")
        seleccion = input("=>")
        if seleccion=='1':
            query = {"nombre":nombreAlumno}
            nuevoNombre = input("Ingrese el nuevo nombre:\t")
            nuevoValor = {"$set":{"nombre":nuevoNombre}}
            alumnos.update_one(query,nuevoValor)
        if seleccion=='2':
            query = {"_id":matriculaAlumno}
            nuevaMatricula = input("Ingresa la nueva matricula:\t")
            nuevoValor = {"$set":{"_id":nuevaMatricula}}
            alumnos.update_one(query,nuevoValor)
        if seleccion=='3':
            query = {"info":infoAlumno}
            nuevaInfo = input("Ingresa el nuevo correo:\t")
            nuevoValor = {"$set":{"info":nuevaInfo}}
            alumnos.update_one(query,nuevoValor)
        if seleccion=='4':
            query = {"password":passAlumno}
            nuevaPass = input("Ingresa la nueva contraseña:\t")
            nuevoValor = {"$set",{"password":nuevaPass}}
            alumnos.update_one(query,nuevoValor)
        if seleccion=='0':
            menu()
def menu():
    print("-------------------------------------------")
    print("-------------------MENU--------------------")
    print("Sistema de administración de cuentas.\n")
    print("1. Registrar usuario(Admin/alumno)\n")
    print("2. Inicio de sesión de usuario\n")
    print("3. Eliminar usuario.\n")
    print("4. Actualizar datos de usuario.\n")
    print("5. Mostrar todos los alumnos.\n")
    print("6. Mostrar todos los administrativos/profesores.\n")
    print("0. Salir.\n")
    opcion = input("Ingresa tu opción:\t")
    if opcion=='1':
        registro()
    if opcion=='2':
        login()
    if opcion=='3':
        print("¿Desea eliminar un Administrativo o un Alumno?\n")
        tipo = input("1.Administrativo\n"
                     "2.Alumno\n")
        if tipo=='1':
            eliminarTipo="Administrativo"
        if tipo=='2':
            eliminarTipo="Alumno"
        else:
            print("Opción inválida\n")
            print("Regresando al menú\n")
            time.sleep(2)
            menu()
        print("Seleccionado:\t"+eliminarTipo)
        matricula = input("Ingrese la matricula:\n")
        eliminarUsuario(matricula,tipo)
    if opcion=='4':
        print("¿Desea actualizar datos de un Administrativo ó de un Alumno?\n")
        tipo = input("1. Administrativo\n"
                     "2. Alumno\n"
                     "=>")
        matricula = input("Ingresa la matricula:\t")
        actualizarDatosUsuario(matricula,tipo)
    if opcion=='5':
        print("****************************************")
        print("*****************ALUMNOS****************")
        estado_db = existeDatabase("UAM")
        estado_col = existeCollecion("alumnos")
        if estado_db and estado_col:
            for datos in alumnos.find():
                print("Nombre:\t"+datos["nombre"])
                print("Matricula:\t"+datos["_id"])
                print("Correo:\t"+datos["info"])
                print("Contraseña:\t"+datos["password"])
                print("****************************************")
    if opcion=='6':
        print("****************************************")
        print("*****************ADMIN******************")
        estado_db2 = existeDatabase("UAM")
        estado_col2 = existeCollecion("administrativos")
        if estado_db2 and estado_col2:
            for datos in admin.find():
                print("Nombre:\t"+datos["nombre"])
                print("Matricula:\t"+datos["_id"])
                print("Correo:\t"+datos["info"])
                print("Contraseña:\t"+datos["password"])
                print("****************************************")
    if opcion=='0':
        print("****************************************")
        print("****************SALIENDO****************")
        exit(0)
while True:
    menu()