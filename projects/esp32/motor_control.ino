/*
1. Half speed normal dir for 2s
2. full speed normal dir for 2s
3. Half speed reverse dir for 2s
4. full speed reverse dir for 2s

*/


// Motor A connections
int ENA = 9;
int IN1 = 8;
int IN2 = 7;

/*
#define ENA 9
#define IN1 8
#define IN2 7
*/
int ENB = 10;
int IN3 = 5;
int IN4 = 4;


void speedcontrol_steps() {
	// Turn off motors
	digitalWrite(IN1, LOW);
	digitalWrite(IN2, LOW);
	digitalWrite(IN3, LOW);
	digitalWrite(IN4, LOW);
	

	//normal direction
	digitalWrite(IN1, HIGH);
	digitalWrite(IN2, LOW);

	analogWrite (ENA, 127);
    delay (2000);
	analogWrite (ENA, 255);
    delay (2000);


	//reverse direction
	digitalWrite(IN1, LOW);
	digitalWrite(IN2, HIGH);
 
	analogWrite (ENA, 127);
    delay (2000);
	analogWrite (ENA, 255);
    delay (2000);

	
	// Now turn off motors
	digitalWrite(IN1, LOW);
	digitalWrite(IN2, LOW);
}

void read () {
  // read the input on analog pin 0:
  int s0 = analogRead (A0);
  int s1 = analogRead (A1);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float v0 = s0;
  float v1 = s1 * (9.0 / 1023);
  // print out the value you read:
  Serial.println (v0);
  //Serial.println (v1);
}

void l () {
	// Turn off motors
	digitalWrite(IN1, LOW);
	digitalWrite(IN2, LOW);
	digitalWrite(IN3, LOW);
	digitalWrite(IN4, LOW);
	
	//straight for 400ms
	digitalWrite(IN1, HIGH);
	digitalWrite(IN2, LOW);
	digitalWrite(IN3, HIGH);
	digitalWrite(IN4, LOW);

	analogWrite (ENA, 100);
	analogWrite (ENB, 100);
  delay (100);

	
	//initiate turn for 50ms
	analogWrite (ENB, 127);
  delay (50);
  
	
	// Turn off motors
	digitalWrite(IN1, LOW);
	digitalWrite(IN2, LOW);
	digitalWrite(IN3, LOW);
	digitalWrite(IN4, LOW);
}


void m () {
  //analogWrite (ENB, 70);
  //analogWrite (ENA, 40);
}



void setup() {
  Serial.begin (1200);

	// Set all the motor control pins to outputs
	pinMode(ENA, OUTPUT);
	pinMode(IN1, OUTPUT);
	pinMode(IN2, OUTPUT);
	pinMode(ENB, OUTPUT);
	pinMode(IN3, OUTPUT);
	pinMode(IN4, OUTPUT);
	
	// Turn off motors - Initial state
  /*
	digitalWrite(IN1, LOW);
 	digitalWrite(IN2, LOW);
  digitalWrite (IN3, LOW);
	digitalWrite (IN4, LOW);
  */


  digitalWrite (IN3, HIGH);
	digitalWrite (IN4, LOW);

  digitalWrite (IN1, HIGH);
	digitalWrite (IN2, LOW);
}


void loop() {
  //speedcontrol_steps();
  //l ();
  //read ();
  //m ();
}




