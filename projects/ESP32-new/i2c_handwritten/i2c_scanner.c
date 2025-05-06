// I2C Scanner Attempting to Use ONLY ESP32 Internal Pull-ups
#include <Arduino.h>
#include <Wire.h>

// Define YOUR ESP32's I2C pins
#define I2C_SDA_PIN 21
#define I2C_SCL_PIN 22

// --- Set very low I2C Clock Frequency for this test ---
#define I2C_FREQ_HZ 1000 // 10kHz

void setup() {
  Serial.begin(115200);
  while (!Serial); // Wait for serial port to connect
  Serial.println("\n--- I2C Scanner Test ---");
  Serial.println("Attempting to use ONLY ESP32 Internal Pull-ups");
  Serial.print("SDA Pin: "); Serial.println(I2C_SDA_PIN);
  Serial.print("SCL Pin: "); Serial.println(I2C_SCL_PIN);
  Serial.print("Target Frequency: "); Serial.print(I2C_FREQ_HZ); Serial.println(" Hz");
  Serial.println("----------------------------------------------------");

  // --- Attempt to Enable Internal Pull-ups BEFORE Wire.begin() ---
  // This is the standard way to enable internal pull-ups for general input,
  // we are testing if it has the desired effect before Wire takes full control.
  Serial.println("Attempting pinMode(pin, INPUT_PULLUP) before Wire.begin()...");
  pinMode(I2C_SDA_PIN, INPUT_PULLUP);
  pinMode(I2C_SCL_PIN, INPUT_PULLUP);
  // Small delay might allow pull-ups to settle, though likely unnecessary
  delay(10);

  // --- Initialize I2C ---
  Serial.println("Calling Wire.begin()...");
  // Wire.begin() configures the pins for I2C (open-drain).
  // Whether the previous pinMode pull-up setting persists effectively
  // or is sufficient is what we are testing.
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);

  // --- Set Clock Speed AFTER Wire.begin() ---
  Serial.print("Setting I2C clock frequency to ");
  Serial.print(I2C_FREQ_HZ);
  Serial.println(" Hz...");
  Wire.setClock(I2C_FREQ_HZ);

  Serial.println("Setup complete. Starting scan loop.");
  Serial.println("----------------------------------------------------");
}

void loop() {
  byte error, address;
  int nDevices;

  Serial.println("Scanning I2C bus...");
  nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    // Attempt to communicate with the device at 'address'
    Wire.beginTransmission(address);
    // endTransmission returns 0 on success (ACK received),
    // 4 on ESP32 usually means NACK (No Acknowledge - device not there or not responding)
    error = Wire.endTransmission();

    if (error == 0) {
      // Device acknowledged!
      Serial.print(">>> I2C device found at address 0x");
      if (address < 16)
        Serial.print("0");
      Serial.print(address, HEX);
      Serial.println(" <<<");
      nDevices++;
    } else if (error == 4) {
      // NACK - This is expected for addresses where no device exists.
      // We don't print anything for this case to keep the output clean.
    } else {
      // Other errors might indicate bus problems (e.g., SCL stuck low)
       Serial.print("! Unexpected Error ");
       Serial.print(error);
       Serial.print(" encountered while probing address 0x");
       if (address<16) Serial.print("0");
       Serial.println(address,HEX);
    }
  } // End of address loop

  // Report summary of scan
  if (nDevices == 0)
    Serial.println("--> Scan complete: No I2C devices found.");
  else
    Serial.print("--> Scan complete: Found "); Serial.print(nDevices); Serial.println(" device(s).");

  Serial.println("----------------------------------------------------");
  delay(5000); // Wait 5 seconds before the next scan
}
