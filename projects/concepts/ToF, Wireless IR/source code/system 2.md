```
#include <IRremote.h>

#define IR_RX 2
#define STEP_PIN 3
#define DIR_PIN 4
#define STEP_COUNT 200
#define STEP_EN 5

IRrecv irReceiver(IR_RX);
decode_results results;


void setup() {
    pinMode(STEP_PIN, OUTPUT);
    pinMode(STEP_EN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);


    Serial.begin(9600);
    irReceiver.enableIRIn(); // Start the IR receiver
}




void loop() {
    if (irReceiver.decode(&results)) { // Check if the received data matches the expected format
        if (results.value != 0xFFFFFFFF) { // Ignore repeat signals
            uint8_t height = results.value & 0xFF;

            // Print the received height for debugging
            Serial.print("Received height: ");
            Serial.println(height);


            // Check if the height exceeds 100 cm (1000 mm)
            if (height > 1000) {
                stepper_action ();
            }
            else {
                Serial.println("Height within limits.");
            }
        }
        irReceiver.resume();
    }
    delay(100);
}




void stepper_action () {
    Serial.println("Height exceeds 100 cm, rotating motor.");

    digitalWrite(STEP_EN, HIGH);
    digitalWrite(DIR_PIN, HIGH); //     Set direction

    // Rotate the motor 90 degrees (adjust steps as necessary)
    for (int i = 0; i < STEP_COUNT; i++) {
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(1000); // Control speed with delay
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(1000);
    }

    digitalWrite(STEP_EN, LOW);
}
```
