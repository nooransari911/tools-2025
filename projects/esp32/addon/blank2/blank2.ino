#define PUSH 22
#define LED1 19
#define LED2 4
#define DELAY_CONST 100

void setup() {
  // put your setup code here, to run once:
  Serial.begin (9600);
  pinMode (PUSH, INPUT_PULLUP);
  pinMode (LED1, OUTPUT);
  pinMode (LED2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int button_status = digitalRead (PUSH);
  
  Serial.println (button_status);
  Serial.println ("SERIALX");

  if (button_status == 1) {
    digitalWrite (LED1, LOW);
    digitalWrite (LED2, LOW);
  }

  else {
    digitalWrite (LED1, HIGH);
    digitalWrite (LED2, HIGH);
  }

  //digitalWrite (LED, HIGH);
  delay (DELAY_CONST);
}
