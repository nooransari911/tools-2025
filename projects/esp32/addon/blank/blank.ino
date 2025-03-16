#define led1 13
#define led2 27


void setup() {
  Serial.begin (9600);
  pinMode (13, OUTPUT);
  pinMode (27, OUTPUT);
}


void loop() {
  const int de = 1000;

  Serial.println("13x HIGH, 27 LOW");
  digitalWrite (led1, HIGH);
  digitalWrite (led2, LOW);
  delay (de);

  Serial.println("13x LOW, 27 HIGH");
  digitalWrite (led1, LOW);
  digitalWrite (led2, HIGH);
  delay (de);
}
