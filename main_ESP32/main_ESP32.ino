#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson-v6.21.5.h>

const char* ssid = "SpartanLuck 117";
const char* password = "numeroPI141592";
const char* serverUrl = "http://192.168.1.64:5000/presion";
const int id_cliente = 1;

// Pines y Variables
const int sensorPin = 2;       // Pin de entrada para el sensor YF-S201
volatile int pulsos = 0;        // Contador de pulsos
float factorCalibracion = 7.5;  // Factor de calibración para el sensor (ajustar según el modelo y pruebas)
float flujo_Lmin = 0;           // Flujo en L/min
float volumen_Litros = 0;       // Volumen total en litros

const int relePin = 33; // Pin donde está conectado el relé
unsigned long tiempoAnterior = 0; // Variable para el cálculo de intervalos de tiempo

void setup() {
  Serial.begin(9600);
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

  //ELECTROVÁLVULA
  Serial.println("Activando electroválvula...");
  //RELEVADOR
  pinMode(relePin, OUTPUT); // Configura el pin del relé como salida
  digitalWrite(relePin, HIGH); // Inicialmente apagado (relé en alto)

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
  delay(5000);
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

    //ENVÍA LOS DATOS A INTERNET
    if (WiFi.status() == WL_CONNECTED) {
    //INICIALIZA LOS SERVIOS HTTP
    HTTPClient http;
    http.begin(serverUrl);
    //CREA LA CABECERA - TIPO JSON
    http.addHeader("Content-Type", "application/json");
    //LLENA EL JSON en texto plano
    String jsonPayload = "{\"presion\":\"" + String(flujo_Lmin) + "\",\"id_cliente\":\""+String(id_cliente)+"\",\"volumen_Litros\":\""+volumen_Litros+"\"}";
    //ENVÍA LA SOLICITUD - TIPO POST
    int httpResponseCode = http.POST(jsonPayload);
    //ESPERA LA RESPUESTA
    if (httpResponseCode > 0) {
      String response = http.getString();
      JSON_Analisys(response);
    } else {
      Serial.print("1.- Error en la conexión: ");
      Serial.println(httpResponseCode);
    }
    //CIERRA EL SERVICIO HTTP
    http.end();
  }
  }
}

void JSON_Analisys(String response) {
    // Reserva espacio para el análisis del JSON
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, response);

    // Verificar si hubo error en el análisis
    if (error) {
        Serial.print(F("Error de JSON: "));
        Serial.println(error.f_str());
        return;
    }

    // Acceder a los valores
    int cod = doc["cod"];           // Obtiene el valor de "cod"
    const char* res = doc["res"];    // Obtiene el valor de "res"
    if(cod == 101){
      Serial.println(res);
      if(digitalRead(relePin) == HIGH){
        Serial.println("Cerrando válvula...");
      }
        digitalWrite(relePin, LOW); // Inicialmente apagado (relé en alto)
    } else {
      if(digitalRead(relePin) == LOW){
        Serial.println("Abriendo válvula...");
      }
        digitalWrite(relePin, HIGH); // Inicialmente apagado (relé en alto)
    }
}

initMain(){
  if (WiFi.status() == WL_CONNECTED) { // Verifica la conexión Wi-Fi
    HTTPClient http;                   // Crear un objeto HTTP

    http.begin("http://192.168.1.64:5000/get-client/"+String(id_cliente));  // Especifica la URL
    int httpResponseCode = http.GET(); // Realiza la petición GET

    if (httpResponseCode > 0) { // Si el código de respuesta es mayor a 0, es exitoso
      String payload = http.getString(); // Obtén el cuerpo de la respuesta
      Serial.println(payload);           // Muestra los datos en el monitor serie
    } else {
      Serial.print("Error en la petición: ");
      Serial.println(httpResponseCode);  // Muestra el código de error si falla
    }

    http.end(); // Cierra la conexión
  } else {
    Serial.println("No conectado a Wi-Fi");
  }
}