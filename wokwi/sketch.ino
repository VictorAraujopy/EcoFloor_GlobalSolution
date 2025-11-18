#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ==========================================
// ⚠️ CONFIGURAÇÃO DE INTERNET
// ==========================================
const char* ssid = "Wokwi-GUEST";
const char* password = "";
// const char* ssid = "SUA_WIFI";
// const char* password = "SUA_SENHA";

// --- CONFIGURAÇÕES API ---
// ⚠️ Confirme se o link do ngrok/devtunnels está atualizado!
String url_base = "https://qw3p1z2g-5000.brs.devtunnels.ms"; 
String sala_id = "101"; 

// --- PINOS ---
#define PIN_PIR 23          
#define PIN_LED_PRESENCA 5  // LED Vermelho (Indica Movimento Local)
#define PIN_LUZ 19          // LED Amarelo (Luz da Sala)
#define PIN_AC 18           // Relé/Motor (Ar Condicionado)
// LED Azul removido conforme solicitado

#define DHTPIN 15           
#define DHTTYPE DHT22       

DHT dht(DHTPIN, DHTTYPE);

int lastState = -1; 
unsigned long lastTime = 0;
unsigned long timerDelay = 2000; 

void setup() {
  Serial.begin(115200);
  
  pinMode(PIN_PIR, INPUT);
  pinMode(PIN_LED_PRESENCA, OUTPUT);
  pinMode(PIN_LUZ, OUTPUT);
  pinMode(PIN_AC, OUTPUT);

  dht.begin();

  digitalWrite(PIN_LUZ, LOW);
  digitalWrite(PIN_AC, LOW);
  digitalWrite(PIN_LED_PRESENCA, LOW);

  Serial.println("\n----------------------------------");
  Serial.println("🚀 INICIANDO SISTEMA (SEM LED AZUL)");
  Serial.print("📡 Conectando WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Wi-Fi Conectado!");
}

void loop() {
  if(WiFi.status() != WL_CONNECTED) return;

  // 1. LEITURA RÁPIDA (SENSOR PIR)
  int presence = digitalRead(PIN_PIR);
  digitalWrite(PIN_LED_PRESENCA, presence ? HIGH : LOW);

  // Se houver mudança de estado (Entrou ou Saiu gente)
  if (presence != lastState) {
    lastState = presence;
    Serial.println("\n🚨 [SENSOR] Movimento detectado -> Enviando...");
    enviarDadosSensor(presence);
  }

  // 2. ATUALIZAÇÃO PERIÓDICA (Para garantir sincronia)
  if ((millis() - lastTime) > timerDelay) {
    receberComandos();
    lastTime = millis();
  }
}

// --- FUNÇÃO OTIMIZADA: Envia e já Atualiza ---
void enviarDadosSensor(int presence) {
    HTTPClient http;
    http.begin(url_base + "/api/dados_sensor");
    http.addHeader("Content-Type", "application/json");

    // Lê temperatura e humidade
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (isnan(t)) t = 20.0; // Valor seguro se falhar

    int luz_estado_atual = digitalRead(PIN_LUZ);
    int ac_estado_atual  = digitalRead(PIN_AC);

    JsonDocument doc;
    doc["sala_id"] = sala_id;
    doc["presenca"] = presence;
    doc["luz_ligada"] = luz_estado_atual;
    doc["ac_ligado"] = ac_estado_atual;
    doc["temperatura"] = t;
    doc["humidade"] = h;

    String json;
    serializeJson(doc, json);

    // Envia POST
    int httpResponseCode = http.POST(json);

    if (httpResponseCode > 0) {
      String payload = http.getString();
      Serial.println("✅ [POST] Enviado. Processando resposta...");
      
      // Atualiza imediatamente com a resposta da API
      JsonDocument responseDoc;
      DeserializationError error = deserializeJson(responseDoc, payload);
      
      if (!error) {
        const char* cmdLuz = responseDoc["comando_luz"];
        const char* cmdAc = responseDoc["comando_ac"];
        
        if (cmdLuz && cmdAc) {
            bool ligarLuz = (String(cmdLuz) == "ON");
            bool ligarAc  = (String(cmdAc) == "ON");

            digitalWrite(PIN_LUZ, ligarLuz ? HIGH : LOW);
            digitalWrite(PIN_AC, ligarAc ? HIGH : LOW);

            Serial.print("⚡ [STATUS] Luz: ");
            Serial.print(cmdLuz);
            Serial.print(" | AC: ");
            Serial.println(cmdAc);
        }
      }
    } else {
      Serial.print("❌ Erro HTTP: ");
      Serial.println(httpResponseCode);
    }
    http.end();
}

void receberComandos() {
  HTTPClient http;
  http.begin(url_base + "/api/comandos/" + sala_id);
  int httpResponseCode = http.GET();

  if (httpResponseCode > 0) {
    String payload = http.getString();
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, payload);

    if (!error) {
      const char* cmdLuz = doc["luz_comando"]; 
      const char* cmdAc  = doc["ac_comando"]; 

      bool ligarLuz = (String(cmdLuz) == "ON");
      bool ligarAc  = (String(cmdAc) == "ON");

      digitalWrite(PIN_LUZ, ligarLuz ? HIGH : LOW);
      digitalWrite(PIN_AC, ligarAc ? HIGH : LOW);
    }
  }
  http.end();
}