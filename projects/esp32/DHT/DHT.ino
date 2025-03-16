#include <DHT.h>
#include <DHT_U.h>
#define DHTTYPE DHT11
#define DHT_PIN 4

DHT dht_object (DHT_PIN, DHT11);


void setup() {
  // put your setup code here, to run once:
  Serial.begin (9600);
  pinMode (DHT_PIN, INPUT);
  dht_object.begin();
  Serial.println("Initializing DHT;");
}


void loop() {
  // put your main code here, to run repeatedly:
  float dht_temperature = dht_object.readTemperature ();
  Serial.println ("Temperature:");
  Serial.println (dht_temperature);
  Serial.printf ("Tempreature: %d", dht_temperature);
}
