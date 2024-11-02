#define LED_BUILTIN 2
/*--------------------*/
#include "DHT.h"
#define DHT11PIN 3
DHT dht(DHT11PIN, DHT11);
/*--------------------*/
#include <Arduino.h>
#include <WiFi.h>
#include <FirebaseESP32.h>
// Provide the token generation process info.
#include <addons/TokenHelper.h>
// Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

// Adding the module of storing data to the NVM (Non volatile memory)
#include <Preferences.h>
Preferences preferences;


/* 1. Define the WiFi credentials */
const char* wifiSSIDs[] = {"B311_EB82", "S23_Ultra", "others"}; // Add your SSIDs here
const char* wifiPasswords[] = {"GL47B9LhDHA", "1234567890", "others"}; // Add the corresponding passwords here

int numberOfNetworks = sizeof(wifiSSIDs) / sizeof(wifiSSIDs[0]);
int currentNetworkIndex = 0;

// For the following credentials, see examples/Authentications/SignInAsUser/EmailPassword/EmailPassword.ino
#define API_KEY "AIzaSyD8k14N4dcioXCrVIOdyJQS2_TBAnp9FD8"
#define DATABASE_URL "https://esp32-895b5-default-rtdb.firebaseio.com/"
#define USER_EMAIL "hamada.hamad.n1663@gmail.com"
#define USER_PASSWORD "001002003"

// Define Firebase Data object
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0; // Ensuring the time and delays
unsigned long counter; // For swapping purposes with real counter
 
void connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  bool connected = false;
  for (int i = 0; i < numberOfNetworks; i++) {
    WiFi.begin(wifiSSIDs[currentNetworkIndex], wifiPasswords[currentNetworkIndex]);
    Serial.print("Attempting to connect to ");
    Serial.print(wifiSSIDs[currentNetworkIndex]);
    Serial.println("...");

    // Try to connect for a maximum of 10 seconds
    int attempts = 10;
    while (WiFi.status() != WL_CONNECTED && attempts > 0) {
      delay(300);
      Serial.print(".");
      attempts--;
    }
    if (WiFi.status() == WL_CONNECTED) {
      connected = true;
      Serial.println("\nWiFi connected.");
      Serial.print("IP address: ");
      Serial.println(WiFi.localIP());
      break;
    } else {
      Serial.println("\nConnection failed.");
      currentNetworkIndex = (currentNetworkIndex + 1) % numberOfNetworks;
    }
  }

  if (!connected) {
    Serial.println("Failed to connect to WiFi. Please check your credentials");
    connectToWiFi(); // Recursion
  }
}


void setup()
{

  Serial.begin(115200);
  /* Start the DHT11 Sensor */
  dht.begin();
  connectToWiFi();
  pinMode(LED_BUILTIN, OUTPUT);
 
  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

  preferences.begin("my-app",false); //Read write mode ("my-app" storage space)
  unsigned long count = preferences.getUInt("count",0);
  counter = count;
  Serial.print("Counter will start from: ");
  Serial.print(count);
  Serial.print("\n...");


  /* Assign the credentials (required) */
  config.api_key = API_KEY;
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;
  config.database_url = DATABASE_URL;
  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; // see addons/TokenHelper.h
  // Comment or pass false value when WiFi reconnection will control by your code or third party library e.g. WiFiManager
  Firebase.reconnectNetwork(true);
  // Since v4.4.x, BearSSL engine was used, the SSL buffer need to be set.
  // Large data transmission may require larger RX buffer, otherwise connection issue or data read time out can be occurred.
  fbdo.setBSSLBufferSize(4096 /* Rx buffer size in bytes from 512 - 16384 */, 1024 /* Tx buffer size in bytes from 512 - 16384 */);

  Firebase.begin(&config, &auth);
  Firebase.setDoubleDigits(5);

  //Setting up the preferences
 
}
void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi connection lost. Reconnecting...");
    connectToWiFi();
  }

  if (Firebase.ready() && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0)) {
    sendDataPrevMillis = millis();
    float humi = dht.readHumidity();
    float temp = dht.readTemperature()*10;
    // Prepare the JSON object with the reading and timestamp
    FirebaseJson json;
    Serial.println(counter);
    String path = "/temp-humi/" + String(counter); // Unique path for each reading 'counter for swapping purposes'
    Serial.println("CURRENT DIR IS ................");
    Serial.println(path);
    json.set("value", counter); // The actual reading
    json.set("Temperature", temp); // The actual reading (from sensor)
    json.set("Humidity", humi);
    json.set("timestamp/.sv", "timestamp"); // Firebase server-side timestamp
    // Send the reading and its timestamp to Firebase
    if (Firebase.set(fbdo, path, json)) {
      Serial.println("Reading and timestamp sent successfully.");
      digitalWrite(LED_BUILTIN,HIGH);
      counter++; // Increment the count (reading value) for the next loop iteration
      preferences.putUInt("count",counter); // Storing the value inside ROM
    } else {
      Serial.println("Failed to send reading and timestamp: " + fbdo.errorReason());
    }
    delay(300); // Small delay before the next loop iteration
    digitalWrite(LED_BUILTIN,LOW);

  }
  // Assuming fbdo is your Firebase Data object and Firebase is properly initialized
}