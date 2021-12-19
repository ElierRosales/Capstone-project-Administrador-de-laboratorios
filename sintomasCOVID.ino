/*
  AUTOR: JORGE ISUR BALDERAS RAMÍREZ
  FECHA: 07-12-2021
  DESCRIPCIÓN: PROGRAMA PARA MEDIR SINTOMAS DE COVID MEDIANTE EL SENSOR
               MAX30102
  CONEXIONES EN HARDWARE(ESP32CAM)
  -5V = 5V (3.3V también funciona)
  -GND = GND
  -SDA = GPIO15
  -SCL = GPIO14
  -INT = Not connected
 
  EL MAX30102 SOPORTA I2C LÓGICA EN 5V Y 3.3V, SE RECOMIENDA ENERGIZAR CON 5V
  A FIN DE TENER MAYOR PRECISIÓN EN LOS DATOS.
*/
/***************************************************************************************
DECLARACIÓN DE BIBLIOTECAS
****************************************************************************************/
#include <Wire.h> //BIBLIOTECA PARA EL MANEJO DE I2C
#include "MAX30105.h" //BIBLIOTECA PARA EL CONTROL DEL MAX3010X
#include "spo2_algorithm.h" //BIBLIOTECA PARA EL ALGORITMO QUE CÁLCULA OXIGENO EN SANGRE
#include <WiFi.h>  // Biblioteca para el control de WiFi
#include <PubSubClient.h> //Biblioteca para conexion MQTT
/***************************************************************************************
DECLARACIÓN DE INSTANCIA DEL SENSOR
****************************************************************************************/
MAX30105 particleSensor;
/***************************************************************************************
DATOS DEL WIFI
****************************************************************************************/
const char* ssid = "INFINITUM3033_2.4";  // Aquí debes poner el nombre de tu red
const char* password = "yYYmteq554";  // Aquí debes poner la contraseña de tu red
/***************************************************************************************
DATOS DEL BROKER MQTT
****************************************************************************************/
const char* mqtt_server = "18.198.240.106"; // Si estas en una red local, coloca la IP asignada, en caso contrario, coloca la IP publica
IPAddress server(18,198,240,106);
/***************************************************************************************
OBJETOS
****************************************************************************************/
WiFiClient esp32Client; // Este objeto maneja los datos de conexion WiFi
PubSubClient client(esp32Client); // Este objeto maneja los datos de conexion al broker

#define MAX_BRIGHTNESS 255

#if defined(__AVR_ATmega328P__) || defined(__AVR_ATmega168__)
uint16_t irBuffer[100]; //infrared LED sensor data
uint16_t redBuffer[100];  //red LED sensor data
#else
uint32_t irBuffer[100]; //infrared LED sensor data
uint32_t redBuffer[100];  //red LED sensor data
#endif

int32_t bufferLength; //LONGITUD DE LOS DATOS
int32_t spo2; //VALOR DEL OXIGENO EN SANGRE
int8_t validSPO2; //INDICADOR PARA MOSTRAR SI EL VALOR DEL SPO2 ES VALIDO
int32_t heartRate; //VALOR DE PULSO CARDIACO
int8_t validHeartRate; //INDICADOR PARA MOSTRAR SI EL VALOR DEL PULSO CARDIACO ES VALIDO

byte readLED = 33; //PARPADEA CON CADA LECTURA DEL SENSOR

void setup()
{
  Serial.begin(115200); // INICIAR LA COMUNICACIÓN SERIAL
  Serial.println("Iniciando...\n");
  Serial.println("LECTOR DE SINTOMAS COVID.\n");
  pinMode(readLED, OUTPUT);
  Serial.print("Conectar a ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password); // Esta es la función que realiz la conexión a WiFi
 
  while (WiFi.status() != WL_CONNECTED) { // Este bucle espera a que se realice la conexión
    digitalWrite (readLED, HIGH);
    delay(500); //dado que es de suma importancia esperar a la conexión, debe usarse espera bloqueante
    digitalWrite (readLED, LOW);
    Serial.print(".");  // Indicador de progreso
    delay (5);
  }
  
  // Cuando se haya logrado la conexión, el programa avanzará, por lo tanto, puede informarse lo siguiente
  Serial.println();
  Serial.println("WiFi conectado");
  Serial.println("Direccion IP: ");
  Serial.println(WiFi.localIP());

  // Si se logro la conexión, encender led
  if (WiFi.status () > 0){
    digitalWrite (readLED, LOW);
  }
  delay (1000); // Esta espera es solo una formalidad antes de iniciar la comunicación con el broker
  // Conexión con el broker MQTT
  client.setServer(server, 1883); // Conectarse a la IP del broker en el puerto indicado
  delay(1500);  // Esta espera es preventiva, espera a la conexión para no perder información

  // Initialize sensor
  Wire.begin(15,14);
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println(F("MAX3010X NO ENCONTRADO. POR FAVOR REVISE EL CABLEADO O LA ALIMENTACIÓN. \n"));
    while (1);
  }

  Serial.println(F("Coloque el dedo en el sensor y aplique presión.\n"));
  Serial.println(F("Presione una tecla cuando este listo.\n"));
  while (Serial.available() == 0) ; //ESPERA A QUE SE APRETE UNA TECLA.
  Serial.read();

  byte ledBrightness = 60; //Options: 0=Off to 255=50mA
  byte sampleAverage = 4; //Options: 1, 2, 4, 8, 16, 32
  byte ledMode = 2; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  byte sampleRate = 100; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411; //Options: 69, 118, 215, 411
  int adcRange = 4096; //Options: 2048, 4096, 8192, 16384

  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configure sensor with these settings
  particleSensor.enableDIETEMPRDY(); //Enable the temp ready interrupt. This is required.

}

void loop()
{
  //Verificar siempre que haya conexión al broker
  if (!client.connected()) {
    reconnect();  // En caso de que no haya conexión, ejecutar la función de reconexión, definida despues del void setup ()
  }// fin del if (!client.connected())
  client.loop(); // Esta función es muy importante, ejecuta de manera no bloqueante las funciones necesarias para la comunicación con el broker
  bufferLength = 100; //buffer length of 100 stores 4 seconds of samples running at 25sps

  //read the first 100 samples, and determine the signal range
  for (byte i = 0 ; i < bufferLength ; i++)
  {
    while (particleSensor.available() == false) //do we have new data?
      particleSensor.check(); //Check the sensor for new data

    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample(); //We're finished with this sample so move to next sample

    Serial.print(F("red="));
    Serial.print(redBuffer[i], DEC);
    Serial.print(F(", ir="));
    Serial.println(irBuffer[i], DEC);
  }

  //CALCULAR EL PULSO CARDIACO Y OXIGENACIÓN DESPUES DE 100 MUESTRAS(PRIMEROS 4 SEGUNDOS)
  maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);

  //CONTINUAMENTE TOMANDO MUESTRAS. PULSO CARDIACO Y OXIGENO SE TOMAN CADA SEGUNDO.
  while (1)
  {
    //DESECHANDO LOS PRIMEROS 25 SETS DE MUESTRAS EN MEMORIA Y RECORRIENDO
    //LAS ULTIMAS 75 MUESTRAS AL PRINCIPIO.
    for (byte i = 25; i < 100; i++)
    {
      redBuffer[i - 25] = redBuffer[i];
      irBuffer[i - 25] = irBuffer[i];
    }

    //take 25 sets of samples before calculating the heart rate.
    for (byte i = 75; i < 100; i++)
    {
      while (particleSensor.available() == false) //¿TENEMOS NUEVAS LECTURAS?
        particleSensor.check(); //MONITOREA EL SENSOR POR NUEVOS DATOS.

      digitalWrite(readLED, !digitalRead(readLED)); //Blink onboard LED with every data read

      redBuffer[i] = particleSensor.getRed();
      irBuffer[i] = particleSensor.getIR();
      particleSensor.nextSample(); //We're finished with this sample so move to next sample

      //send samples and calculation result to terminal program through UART
      Serial.print(F("red="));
      Serial.print(redBuffer[i], DEC);
      Serial.print(F(", ir="));
      Serial.print(irBuffer[i], DEC);

      Serial.print(F(", PULSO CARDIACO=\n"));
      Serial.print(heartRate, DEC);
      char pulso[10];
      itoa(heartRate,pulso,10);//CONVERTIR INT-->CHAR[] PARA ENVIAR POR MQTT
      client.publish("isur/pulso",pulso);

      Serial.print(F(", PULSO CARDIACO VALIDO=\n"));
      Serial.print(validHeartRate, DEC);

      Serial.print(F(", OXIGENO EN SANGRE=\n"));
      Serial.print(spo2, DEC);
      char oxigeno[10];
      itoa(spo2,oxigeno,10);//CONVERTIR INT-->CHAR[] PARA ENVIAR POR MQTT
      client.publish("isur/oxigeno",oxigeno);

      Serial.print(F(", OXIGENO EN SANGRE VALIDO=\n"));
      Serial.println(validSPO2, DEC);

      float temperature = particleSensor.readTemperature();
      char tempArray[8];
      Serial.print(",Temperatura=\n")
      Serial.print(temperature, 4);
      dtostrf(temperature,1,2,tempArray);//CONVERTIR FLOAT-->CHAR[] PARA ENVIAR POR MQTT
      client.publish("isur/temp",tempArray);

      if((heartRate<validHeartRate)or(spo2<validSPO2)or(temperature>=37)){
        Serial.println("Usted presenta sintomas de COVID-19\n");
      }
      else{
        Serial.println("Sintomas Normales\n");
      }
      delay(1500);
    }

    //After gathering 25 new samples recalculate HR and SP02
    maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
  }
}
// Función para reconectarse
void reconnect() {
  // Bucle hasta lograr conexión
  while (!client.connected()) { // Pregunta si hay conexión
    Serial.print("Tratando de contectarse...");
    // Intentar reconexión
    if (client.connect("ESP32CAMClient")) { //Pregunta por el resultado del intento de conexión
      Serial.println("Conectado");
      client.subscribe("rikoudousennin7"); // Esta función realiza la suscripción al tema
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
