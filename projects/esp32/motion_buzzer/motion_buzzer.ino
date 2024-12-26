#define BUZZ 5
#define PIR 23
//32, 27, 14


void setup() {
  // put your setup code here, to run once:
  Serial.begin (9600);
  pinMode (BUZZ, OUTPUT);
  pinMode (PIR, INPUT);
  digitalWrite (BUZZ, LOW);

}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  digitalWrite (BUZZ, LOW);
  delay (400);
  digitalWrite (BUZZ, HIGH);
  delay (400);
  */

  int pir_state = digitalRead (PIR);
  digitalWrite (BUZZ, LOW);

  
  if (pir_state == HIGH) {
    // MOTION
    buzz_motion ();
  }
  else {
    // NO MOTION
    Serial.println ("NO MOTION DETECTED");
  }
  
}


void buzz_motion () {
  for (int i=0; i<6; i++){ 
    Serial.println ("MOTION DETECTED");
    digitalWrite (BUZZ, LOW);
    delay (200);
    digitalWrite (BUZZ, HIGH);
    delay (200);
  }
}
