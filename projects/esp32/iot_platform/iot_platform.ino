#define BLYNK_TEMPLATE_ID "TMPL3Vs-Eqeik"
#define BLYNK_TEMPLATE_NAME "light relay"
#define BLYNK_AUTH_TOKEN "5V9BzUbaXGA8pl67Gu35DALJpXjOiDcY"

#define BLYNK_PRINT Serial

#define RELAY_PIN 12
//#define SW 10
#define RELAY_TURN_ON LOW
#define RELAY_TURN_OFF HIGH

#include <BlynkSimpleEsp32.h>
#include <WiFi.h>
#include <Blynk.h>

/*
#include <DHT.h>
#include <DHT_U.h>

#define DHTTYPE DHT11
#define dhtPin 19
//object dht of DHT class,
DHT dht(dhtPin, DHTTYPE);
float temperature =0.0, humidity=0.0;
*/

const char SSID[] = "Rushikesh 5G";
const char PASS[] = "zxcvbnmz";


BLYNK_WRITE(V0) {
  int SW = param.asInt(); // Get the value from the Blynk app (V0)
  Serial.println ("Switch change state:    ");
  Serial.print (SW);
}



void setup() {
  // put your setup code here, to run once:
  pinMode (RELAY_PIN, OUTPUT);
  //pinMode (SW, INPUT_PULLUP);

  digitalWrite (RELAY_PIN, RELAY_TURN_OFF);


  Serial.begin (9600);
  Blynk.begin (BLYNK_AUTH_TOKEN, SSID, PASS);
  Serial.println ("Start");
  delay (2000);

}




void loop() {
  // put your main code here, to run repeatedly:
  Blynk.run ();
  /*
  temperature = dht.readTemperature();
  humidity= dht.readHumidity();

  Serial.println("Temperature:  ");
  Serial.print(temperature);
  Serial.println("Humidity:  ");
  Serial.print(humidity);
  Blynk.virtualWrite(V0,temperature);
  Blynk.virtualWrite(V1,humidity);
  */
  




  digitalWrite (RELAY_PIN, HIGH);
  Serial.println (digitalRead (RELAY_PIN));
  delay (1000);

  digitalWrite (RELAY_PIN, LOW);
  Serial.println (digitalRead (RELAY_PIN));
  delay (1000);

  //int sw_state = Blynk.virtualRead (V0);
  //Serial.println (V0);
  /*
  if (sw_state == 1)  {
    Serial.println ("ON");
    digitalWrite (SW, RELAY_TURN_ON);
    delay (400);
    digitalWrite (RELAY_PIN, RELAY_TURN_OFF);
  }
  else {
  }
  */
}