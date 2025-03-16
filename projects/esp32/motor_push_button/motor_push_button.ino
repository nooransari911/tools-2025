#define ENA 14
#define IN1 26
#define IN2 25

#define PUSH1 27
#define PUSH2 33


void off () {
  digitalWrite(IN1, LOW);
 	digitalWrite(IN2, LOW);
}

void forward (int speed) {
  analogWrite (ENA, speed);
  digitalWrite(IN1, HIGH);
 	digitalWrite(IN2, LOW);
}

void reverse (int speed) {
  analogWrite (ENA, speed);
  digitalWrite(IN1, LOW);
 	digitalWrite(IN2, HIGH);
}




void setup() {
  // put your setup code here, to run once:
  Serial.begin (9600);
  pinMode(ENA, OUTPUT);
	pinMode(IN1, OUTPUT);
	pinMode(IN2, OUTPUT);

  pinMode (PUSH1, INPUT_PULLUP);
  pinMode (PUSH2, INPUT_PULLUP);

  digitalWrite(IN1, LOW);
 	digitalWrite(IN2, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  off ();
  forward (255);
  Serial.println ("Fast");
  delay (1000);

  forward (127);
  Serial.println ("Slow");
  delay (1000);

  forward (0);
  Serial.println ("Stop");
  delay (1000);
  */
  //reverse (255);

  int push1_state = digitalRead (PUSH1);
  int push2_state = digitalRead (PUSH2);

  if (push1_state == 0 && push2_state == 1) {
    forward (255);
    Serial.println (push1_state);
    Serial.println ("Forward");
    delay (2000);
  }

  if (push2_state == 0 && push1_state == 1) {
    reverse (255);
    Serial.println (push2_state);
    Serial.println ("Reverse");
    delay (2000);
  }

  else {
    off ();
    Serial.println ("OFF");
  }

}
