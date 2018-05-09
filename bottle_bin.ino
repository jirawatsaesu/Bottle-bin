// Import library
#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x3F, 16, 2);

int motion = 13;  // Digital pin D7
int buzzer = 12;  // Digital pin D6

int state;

const char *ssid = "PleumJira";        // Your wifi
const char *password = "1357913579";   // Your password

// Web/Server address to read/write from
const char *host = "172.20.10.10";

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_OFF);        // Prevents reconnection issue (taking too long to connect
  WiFi.mode(WIFI_STA);        // This line hides the viewing of ESP as wifi hotspot
  
  WiFi.begin(ssid, password); // Connect to WiFi router
  Serial.println("");

  // Wait for connection
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  // If connection successful show IP address in serial monitor
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP()); // IP address assigned to your ESP

  pinMode(motion, INPUT);
  pinMode(buzzer, OUTPUT);
}

void loop() {
  state = digitalRead(motion);  // Read values from motion sensor
  if (state == HIGH) {
    Serial.println("Motion detected!");

    // Generate random code
    String code, Link, getData;
    for (int i=0; i <= 3; i++){
      code += String(random(9));
    }

    // Initialize the LCD
    lcd.begin();

    // Turn on the blacklight and print a message.
    lcd.backlight();
    lcd.print("CONGRATULATIONS!");
    lcd.setCursor(0,1);
    lcd.print("   CODE: " + code);

    HTTPClient http;                          // Declare object of class HTTPClient
    // Get request
    getData = "?code=" + code;
    Link = "http://172.20.10.10:5000/addcode" + getData;
    Serial.println(Link);
    http.begin(Link);                         // Specify request destination
    
    int httpCode = http.GET();                // Send request
    String payload = http.getString();        // Get the response payload

    Serial.println(httpCode);                 // Print HTTP return code
    Serial.println(payload);                  // Print request response payload

    http.end();                               // Close connection
    digitalWrite(buzzer, HIGH);
    delay(5000);
    digitalWrite(buzzer, LOW);
    lcd.clear();
    lcd.noBacklight();
  }
}






