"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Autor: Juan Elier Rosales Rosas
Fecha: 10/02/22
Descripción: Programa para leer un dispositivo NFC mediante 
	     el sensor PN532.
	
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################################
#Declaración de modulos
###################################
import paho.mqtt.client as mqtt
import time
import binascii

###################################
#Declaración de bibliotecas
###################################

from pn532pi import Pn532, pn532
from pn532pi import Pn532I2c
from pn532pi import Pn532Spi
from pn532pi import Pn532Hsu

###################################
#Elección de interface a usar.
#Para seleccionar coloca el valor true
###################################
SPI = False
I2C = False
HSU = True
###################################
#Comprobación de los valores para la interfaz
###################################
if SPI:
    PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
    nfc = Pn532(PN532_SPI)
# Cuando el número después de #elif es 1, se deberá poner en HSU.
elif HSU:
    PN532_HSU = Pn532Hsu(0)
    nfc = Pn532(PN532_HSU)

# Cuando el número después de #if & #elif se configura con
# 0, se debera poner en modo I2C
elif I2C:
    PN532_I2C = Pn532I2c(1)
    nfc = Pn532(PN532_I2C)

###################################
#Llamada para cuando el cliente recibe respuesta del servidor
###################################
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.connect("187.200.114.169", 1883, 60) #Aquí cambias por la ip o dirección de tu broker

def setup():
    nfc.begin()

    versiondata = nfc.getFirmwareVersion()
    if not versiondata:
        print("Didn't find PN53x board")
        raise RuntimeError("Didn't find PN53x board")  # halt

    # Confirmación de sensor encontrado
    print("Lector PN5 encontrado {:#x}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
                                                                (versiondata >> 8) & 0xFF))
    # Configura el número maximo de intentos para leer alguna tarjeta
    #Esto previene que se espere una tarjeta siempre
    #Está definido por default por el PN532
    nfc.setPassiveActivationRetries(0xFF)

    # Configura para leer los tags RFID
    nfc.SAMConfig()

def loop():
    # Se espera un tag de tipo ISO14443A (Mifare, etc.). Cuando una es encontrada
    # 'uid'se llena con el UID, y la longitud del UID indica que
    # si el uid es 4 bytes (Mifare Classic) o 7 bytes (Mifare Ultralight)

    success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

    if (success):
        print("Tarjeta leida!") #Se leyó con exito la tarjeta
        uidconv = binascii.b2a_hex(uid);#Regresa de representación hexadecimal a binario
        uidstr = uidconv.decode();
        print("UID:",uidstr)
	#Aquí cambias el cliente/tema con los tuyos
        client.publish('isur/uid', payload = uidstr, qos=0,retain=False)
        time.sleep(1)
        return True
    else:
        #Tiempo de espera del PN532
        print("Timed out waiting for a card")
        return False



if __name__ == '__main__':
    setup()
    found = loop()
    while not found:

      found = loop()