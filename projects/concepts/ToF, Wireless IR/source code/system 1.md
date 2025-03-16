```
#include <Wire.h>
#include <VL53L0X.h>
#include <IRremote.h>

#define IR_PROXIMITY_PIN 2  // IR proximity sensor pin
//define IR_TX_EN 3     // IR transmitter module enable pin
#define IR_TX 4        // IR transmitter module data pin


VL53L0X sensor;
IRsend irSender (IR_TX);




void setup() {
    pinMode (IR_PROXIMITY_PIN, INPUT);
    pinMode (IR_TX_EN, OUTPUT);
    pinMode (IR_TX, OUTPUT);

    Serial.begin (9600);
    Wire.begin ();
    irSender.begin();
    sensor.init ();
    sensor.setTimeout (500);
}




void loop() {
    int human_presence = digitalRead (IR_PROXIMITY_PIN);

    if (human_presence == HIGH) { // Human detected
        uint8_t height = sensor_height ();


        if (height > 0) {
            //digitalWrite (IR_TX_EN, HIGH); // Enable the IR module
            delay(50);
            irSender.sendNEC (height, 8);
            //digitalWrite (IR_TX_EN, LOW);
        }
    }

    delay(100);
}





uint8_t sensor_height () {
    uint8_t height = sensor.readRangeSingleMillimeters();
    height = constrain(height, 0, 255);
    if (sensor.timeoutOccurred()) {
        Serial.println("Timeout");
        return 0;
    }
    return height;
}

```
