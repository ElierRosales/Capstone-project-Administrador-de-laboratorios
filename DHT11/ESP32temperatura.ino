/*
    AUTOR: Jorge Isur Balderas Ramírez
    FECHA: 25/08/2021
    DISPOSITIVO: ESP32CAM + DHT11
    DESCRIPCIÓN: Programa que muestra la temperatura medida por el DHT11
    GPIO DESCRIPTION:
    DHT11 DATA-------------->GPIO2
    DHT11 POWER------------->3.3V
    DHT11 GND--------------->GND
    LED_OK(VERDE)----------->GPIO13
    LED_WARNING(AMARILLO)--->GPIO14
    LED_FATAL(ROJO)--------->GPIO15
    LED_STATUS-------------->GPIO33{
      INVERSO: ON--->LOW
               OFF-->HIGH
      NO EXPUESTO: SOLO SE PUEDE MANIPULAR MEDIANTE SOFTWARE.
    }

*/
//BIBLIOTECAS
#include "DHT.h"
#include <WiFi.h>  // Biblioteca para el control de WiFi
#include <PubSubClient.h> //Biblioteca para conexion MQTT
// DEFINIMOS LOS PINES QUE SE USARÁN
#define DHTPIN 2
#define DHTTYPE DHT11   // DHT 11
#define LED_OK 13
#define LED_WARNING 14
#define LED_FATAL 15
#define LED_STATUS 33
//DATOS DEL GUAIFAI
const char* ssid = "INFINITUM3033_2.4";//CAMBIAR POR TU NOMBRE DE RED.
const char* password = "yYYmteq554"; //tu contraseña de wifi
//DATOS DEL BROKER MQTT
//en caso de usar broker publico, actualizar la ip.
const char* mqtt_server = "18.198.240.106";
IPAddress server(18,198,240,106);
//objetos
WiFiClient esp32Client;
PubSubClient client(esp32Client);
//inicializar el DHT
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  Serial.println(F("Lector de temperatura y humedad iniciado."));
  pinMode (LED_OK, OUTPUT);//Specify that LED pin is output
  pinMode (LED_WARNING, OUTPUT);//Specify that LED pin is output
  pinMode (LED_FATAL, OUTPUT);//Specify that LED pin is output
  Serial.println();
  Serial.println();
  Serial.print("Conectar a ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password); // Esta es la función que realiz la conexión a WiFi
 
  while (WiFi.status() != WL_CONNECTED) { // Este bucle espera a que se realice la conexión
    digitalWrite (LED_STATUS, HIGH);
    delay(500); //dado que es de suma importancia esperar a la conexión, debe usarse espera bloqueante
    digitalWrite (LED_STATUS, LOW);
    Serial.print(".");  // Indicador de progreso
    delay (5);
  }
  
  // Cuando se haya logrado la conexión, el programa avanzará, por lo tanto, puede informarse lo siguiente
  Serial.println();
  Serial.println("WiFi conectado");
  Serial.println("Direccion IP: ");
  Serial.println(WiFi.localIP());
  delay (1000); // Esta espera es solo una formalidad antes de iniciar la comunicación con el broker
  // Conexión con el broker MQTT
  client.setServer(server, 1883); // Conectarse a la IP del broker en el puerto indicado
  client.setCallback(callback); // Activar función de CallBack, permite recibir mensajes MQTT y ejecutar funciones a partir de ellos
  delay(1500);  // Esta espera es preventiva, espera a la conexión para no perder información
  dht.begin();
}

void loop() {
  //Verificar siempre que haya conexión al broker
  if (!client.connected()) {
    reconnect();  // En caso de que no haya conexión, ejecutar la función de reconexión, definida despues del void setup ()
  }// fin del if (!client.connected())
  client.loop(); // Esta función es muy importante, ejecuta de manera no bloqueante las funciones necesarias para la comunicación con el broker
  // Wait a few seconds between measurements.
  delay(5000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  //float f = dht.readTemperature(true);
  String hum = String(h);
  String temp = String(t);
  //conversion a char[]
  char* humedad = hum.toCharArray();
  char* celsius = temp.toCharArray();
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println(F("ERROR AL REGISTRAR LOS DATOS DEL SENSOR!"));
    return;
  }
  if (t<25)
  {
      digitalWrite(LED_OK,HIGH);
      digitalWrite(LED_WARNING,LOW);
      digitalWrite(LED_FATAL,LOW);
  }
  if (t>=25 && t<30)
  {
      digitalWrite(LED_WARNING,HIGH);
      digitalWrite(LED_FATAL,LOW);
      digitalWrite(LED_OK,LOW);
  }
  else{
      digitalWrite(LED_OK,LOW);
      digitalWrite(LED_WARNING,LOW);
      digitalWrite(LED_FATAL,HIGH);
  }
  Serial.print(F("Humedad: "));
  Serial.print(h);
  Serial.print(F("%  Temperatura: "));
  Serial.print(t);
  Serial.print(F("°C \n"));
  client.publish("isur/humedad",humedad);
  client.publish("isur/temp",temp);
}
// Función para reconectarse
void reconnect() {
  // Bucle hasta lograr conexión
  while (!client.connected()) { // Pregunta si hay conexión
    Serial.print("Tratando de contectarse...");
    // Intentar reconexión
    if (client.connect("ESP32CAMClient")) { //Pregunta por el resultado del intento de conexión
      Serial.println("Conectado");
    }// fin del  if (client.connect("ESP32CAMClient"))
    else {  //en caso de que la conexión no se logre
      Serial.print("Conexion fallida, Error rc=");
      Serial.print(client.state()); // Muestra el codigo de error
      Serial.println(" Volviendo a intentar en 5 segundos");
      // Espera de 5 segundos bloqueante
      delay(5000);
      Serial.println (client.connected ()); // Muestra estatus de conexión
    }// fin del else
  }// fin del bucle while (!client.connected())
}// fin de void reconnect()