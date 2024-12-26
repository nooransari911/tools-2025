#include <Arduino.h>
#include <ESP32Servo.h>
#define SERVO_PWM 33
#define TIME_DELAY 2000
#define ANGLE_LIMIT 180



Servo serv;

void setup() {
  // put your setup code here, to run once:
  serv.attach (SERVO_PWM);
}

void loop() {
  // put your main code here, to run repeatedly:
  int angle = 0;


  for (angle = 0; angle <= ANGLE_LIMIT; angle++) {
    serv.write (angle);  // Set the servo position
    delay (TIME_DELAY / ANGLE_LIMIT);      // Delay for smooth transition (3 seconds for 90 degrees)
  }



  for (angle = ANGLE_LIMIT; angle >= 0; angle--) {
    serv.write (angle);  // Set the servo position
    delay (TIME_DELAY / ANGLE_LIMIT);      // Delay for smooth transition (3 seconds for 90 degrees)
  }
}
