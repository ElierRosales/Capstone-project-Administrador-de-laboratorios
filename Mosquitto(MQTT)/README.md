# Mosquitto
Mosquito es un proyecto que proporciona un broker **MQTT** de código abierto.

![mosquitto](imagenes/mosquitto.png)
# MQTT
## ¿Qué es MQTT?
Es un protocolo de comunicación M2M (machine-to-machine) donde dispositivos se comunican entre sí utilizando un patrón publicar/suscribir. Es muy ligero, por lo que es de especial utilidad en casos donde se requiere un muy bajo consumo de energía y ancho de banda.
## Funcionamiento de MQTT
Cuando hablamos de MQTT, tenemos que nombrar sus elementos.
- Cliente
  
  Cualquier dispositivo que se encuentre conectado al broker que pueda suscribirse o publicar.
- Broker
  
  Es el servidor el cual maneja los mensajes publicados por clientes y los distribuye a los clientes suscritos.
- Publicar
  
  Es el envío de información a traves del broker.
- Suscribir
  
  Es la manera de recibir la información publicada en un "canal" específico.
- Tema
  
  El tema vendría siendo un destino, es el lugar donde queremos que la información sea publicada, y pueda ser recibida por cualquiera que este suscrito al tema.

# Materiales
- Raspberry Pi 3 Model B+
- Una red(local/internet)
- Abrir los puertos de tu modem(opcional)
# Instalación
## Raspberry Pi 3 Model B+ (Debian)
1. Abriremos una terminal, puedes abrirla directamente desde tu raspberry o utilizando un cliente ssh.
2. Correremos el siguiente comando, asegurate de tener permisos de administrador.
   
   `sudo apt update && sudo apt upgrade`

   Este comando lo que hará sera que con **update** actualizaremos la lista de repositorios y la lista de versiones de los paquetes que hayan sido actualizados por los desarrolladores, mientras que con **upgrade** actualizaremos dichos paquetes.
3. Posteriormente correremos el siguiente comando:
   
   `sudo apt install -y mosquitto mosquitto-clients`

   En este comando instalara mosquitto y las utilidades para poder publicar y suscribirnos al broker.

# Probar la instalación de Mosquitto.
Finalmente puedes probar que mosquitto se instaló mediante el siguiente comando

`mosquitto -v`
# Activar Mosquitto
Una vez instalado, tenemos 2 opciones para poder iniciar el servicio de mosquitto

- sudo systemctl enable --now mosquitto.service
  
  Iniciará el servicio en este momento y se iniciará automáticamente en cada reinicio o inicio de sesión.
- sudo systemctl enable mosquitto.service
  
  El servicio se iniciará automáticamente a partir del siguiente reinicio o inicio de sesión.
- sudo systemctl start mosquitto.service
  
  El servicio se iniciará en este momento pero **NO** se activará el inicio automático en cada reinicio o inicio de sesión.
