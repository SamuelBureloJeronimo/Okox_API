#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson-v6.21.5.h>

const char* ssid = "SpartanLuck 117";
const char* password = "numeroPI141592";
const String serverUrl = "http://192.168.239.162:5000";

int id_cliente = -1;
String macAddress = "";  // Variable global para almacenar la dirección MAC
float volumen_Litros = 0.0;       // Volumen total en litros
// Pines y Variables
const int sensorPin = 15;       // Pin de entrada para el sensor YF-S201
volatile int pulsos = 0;        // Contador de pulsos
float factorCalibracion = 3.5;  // Factor de calibración para el sensor (ajustar según el modelo y pruebas)
float flujo_Lmin = 0.0;           // Flujo en L/min

const int relePin = 23; // Pin donde está conectado el relé
unsigned long tiempoAnterior = 0; // Variable para el cálculo de intervalos de tiempo
bool limit_Supered = true;

void setup() {
  Serial.begin(9600);  
  
  
  //ELECTROVÁLVULA
  //RELEVADOR
  pinMode(relePin, OUTPUT); // Configura el pin del relé como salida
  digitalWrite(relePin, HIGH); // Inicialmente apagado (relé en alto)
  
  // MODULO DE CONEXIÓN A INTERNET
  WiFi.begin(ssid, password);
  delay(3000);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Conectado a WiFi");
  Serial.print("Ip addres: ");
  Serial.println(WiFi.localIP());
  macAddress = WiFi.macAddress();  // Obtiene la dirección MAC
  Serial.println(macAddress);

  initMain();

  // Crear tarea para manejar peticiones HTTP
  xTaskCreatePinnedToCore(
    sendHttpTask,     // Función de la tarea
    "HTTP_Task",      // Nombre de la tarea
    8192,             // Tamaño del stack
    NULL,             // Parámetros para la tarea
    1,                // Prioridad de la tarea
    NULL,             // Handle de la tarea
    1                 // Core en el que se ejecutará (0 o 1)
  );

  //SENSOR DE FLUJO DE AGUA
  pinMode(sensorPin, INPUT_PULLUP);    // Configura el pin del sensor como entrada
  attachInterrupt(digitalPinToInterrupt(sensorPin), contarPulsos, FALLING); // Interrupción para contar pulsos
}

// Función de interrupción para contar pulsos
void contarPulsos() {
  pulsos++;
}

void loop() {
  SendData_WaterFlow();
  delay(1000);
}

void SendData_WaterFlow()
{
  // Calcula el flujo de agua cada segundo
  unsigned long tiempoActual = millis();
  if (tiempoActual - tiempoAnterior >= 1000) {
    tiempoAnterior = tiempoActual;

    // Calcula el flujo de agua en L/min
    flujo_Lmin = (pulsos / factorCalibracion); // Flujo en litros por minuto
    volumen_Litros += flujo_Lmin / 60;         // Acumula el volumen total en litros

    // Muestra el flujo y volumen total en el monitor serial
    Serial.print("Flujo: ");
    Serial.print(flujo_Lmin);
    Serial.print(" L/min\tVolumen Total: ");
    Serial.print(volumen_Litros);
    Serial.println(" L");

    // Reinicia el contador de pulsos para el siguiente cálculo
    pulsos = 0;
  }
}

void OpenCloseValvula(String response) {

    // Reserva espacio para el análisis del JSON
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, response);

    // Verificar si hubo error en el análisis
    if (error) {
        Serial.print(F("Error de JSON: "));
        Serial.println(error.f_str());
        return;
    }
    
    if(doc["st"] == 901){
        limit_Supered = true;
        digitalWrite(relePin, HIGH); // Inicialmente apagado (relé en alto)
        Serial.println("Cerrando válvula...");
          Serial.println("LOS SERVICIOS FUERON SUSPENDIDOS.");
      return;
    } 
    
    // Acceder a los valores
    int cod = doc["cod"];           // Obtiene el valor de "cod"
    const char* res = doc["res"];    // Obtiene el valor de "res"
    if(cod == 101){
      Serial.println(res);
      digitalWrite(relePin, LOW); // Inicialmente apagado (relé en alto)
      Serial.println("Abriendo válvula...");
    } else {
      digitalWrite(relePin, HIGH); // Inicialmente apagado (relé en alto)
      Serial.println("Cerrando válvula...");
      Serial.println("LIMITE DIARIO ALCANZADO.");
    }
}

void initMain(){
  if (WiFi.status() == WL_CONNECTED) { // Verifica la conexión Wi-Fi
    HTTPClient http;                   // Crear un objeto HTTP

    //CREA LA CABECERA - TIPO JSON
    String encodedMac = urlEncode(macAddress);
    String url = serverUrl+"/initialitation/"+encodedMac;
    http.begin(url);  // Especifica la URL
    http.setTimeout(30000); // Establece el tiempo de espera a 30 segundos
    int httpResponseCode = http.GET(); // Realiza la petición GET

    if (httpResponseCode == 200) { // Si el código de respuesta es mayor a 0, es exitoso
      String payload = http.getString(); // Obtén el cuerpo de la respuesta
      Serial.println(payload);// Muestra los datos en el monitor serie
      // Reserva espacio para el análisis del JSON
      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, payload);

      // Verificar si hubo error en el análisis
      if (error) {
          Serial.print(F("Error de JSON: "));
          Serial.println(error.f_str());
      }

      if(doc["st"]){
        if(doc["st"] == 901){
          id_cliente = doc["id_cliente"];          
          digitalWrite(relePin, HIGH); // Inicialmente apagado (relé en alto)
          Serial.println("LIMITE DIARIO ALCANZADO.");
          Serial.println("Cerrando válvula...");
          volumen_Litros = doc["volumen_Litros"];
        }

      } else {
        id_cliente = doc["id_cliente"];
        volumen_Litros = doc["volumen_Litros"];
          Serial.println("EL DISPOSITIVO INICIO CORRECTAMENTE.");
          digitalWrite(relePin, LOW); // Inicialmente apagado (relé en alto)
          Serial.println("Abriendo válvula...");
      }


    } else {
      Serial.print("Error en la petición: ");
      Serial.println(httpResponseCode);  // Muestra el código de error si falla
    }

    http.end(); // Cierra la conexión
  } else {
    Serial.println("No conectado a Wi-Fi");
  }
}

// Función para codificar caracteres especiales en la URL
String urlEncode(String str) {
  String encoded = "";
  for (int i = 0; i < str.length(); i++) {
    char c = str.charAt(i);
    if (c == ':') {
      encoded += "%3A";  // Reemplazar ':' por '%3A'
    } else if (c == ' ') {
      encoded += "%20";  // Reemplazar espacios por '%20'
    } else {
      encoded += c;  // Otros caracteres se mantienen igual
    }
  }
  return encoded;
}





void sendHttpTask(void *parameter) {
  while (true) {
    if (WiFi.status() == WL_CONNECTED) {
      //INICIALIZA LOS SERVIOS HTTP
      HTTPClient http;
      http.begin(serverUrl+"/presion");
      http.setTimeout(30000); // Establece el tiempo de espera a 30 segundos
      //CREA LA CABECERA - TIPO JSON
      http.addHeader("Content-Type", "application/json");
      //LLENA EL JSON en texto plano
      String jsonPayload = "{\"presion\":\"" + String(flujo_Lmin) + "\",\"id_cliente\":\""+String(id_cliente)+"\",\"volumen_Litros\":\""+volumen_Litros+"\"}";
      Serial.println(jsonPayload);
      //ENVÍA LA SOLICITUD - TIPO POST
      int httpResponseCode = http.POST(jsonPayload);
      //ESPERA LA RESPUESTA
      if (httpResponseCode == 200) {
        String response = http.getString();
        Serial.println(response);
        OpenCloseValvula(response);
      } else {
        Serial.print("1.- Error en la conexión: ");
        Serial.println(httpResponseCode);
      }
      //CIERRA EL SERVICIO HTTP
      http.end();
    } else {
      Serial.println("WiFi desconectado");
    }

    vTaskDelay(1000 / portTICK_PERIOD_MS);  // Espera un segundo
  }
}