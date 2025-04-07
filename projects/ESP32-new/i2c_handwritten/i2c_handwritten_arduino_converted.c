#include <Arduino.h>
#include <Wire.h> // Include the Arduino I2C library

// --- User Configuration ---
// Define YOUR ESP32's I2C pins if not using defaults (GPIO 21/22)
#define I2C_SDA_PIN 21
#define I2C_SCL_PIN 22

// Define I2C Clock Frequency (e.g., 100kHz or 400kHz)
#define I2C_FREQ_HZ 400000 // 400kHz

// --- TMP102 Sensor Definitions ---
#define TMP102_ADDR 0x48 // 7-bit I2C address (0b1001000) - Check your sensor module!

// Register addresses
#define POINTER_TEMP      0x00
#define POINTER_CONFIG    0x01
#define POINTER_TLOW      0x02
#define POINTER_THIGH     0x03

// Temperature Threshold values (Raw values for the registers)
// TLOW register (90°C = 90 / 0.0625 = 1440 = 0x5A0. Left shift 4 = 0x5A00)
#define TLOW_VALUE  0x5A00
// THIGH register (120°C = 120 / 0.0625 = 1920 = 0x780. Left shift 4 = 0x7800)
#define THIGH_VALUE 0x7800

// --- GPIO Pin Definitions ---
#define RELAY_CH1_PIN   18 // Output Pin for Relay Channel 1 (Active HIGH assumed)
#define RELAY_CH2_PIN   19 // Output Pin for Relay Channel 2 (Active HIGH assumed)
#define ENABLE_PIN      20 // Output Pin for enabling external component
#define ALERT_PIN       4  // Input Pin for Alert signal from TMP102

// --- Global Variables ---
// volatile is crucial for variables shared between ISR and main loop
volatile bool alert_occurred_flag = false;
// State variable to track if relays were turned off due to an alert
bool relays_off_by_alert = false;

// --- ISR Function ---
// Minimal ISR: Triggered on FALLING edge (HIGH to LOW transition) of ALERT_PIN.
// Just sets a flag for the main loop to handle. Very fast and safe.
void ICACHE_RAM_ATTR alertPinISR() {
    alert_occurred_flag = true;
}

// --- Helper Function: Write to a TMP102 Register ---
// Sends 2 bytes of data to the specified register address on the TMP102.
// Returns true on success, false on I2C communication error.
bool writeTmp102Register(uint8_t regAddr, uint16_t value) {
    uint8_t msb = (value >> 8) & 0xFF;
    uint8_t lsb = value & 0xFF;

    Wire.beginTransmission(TMP102_ADDR);
    Wire.write(regAddr); // Point to the register we want to write to
    Wire.write(msb);     // Send the Most Significant Byte
    Wire.write(lsb);     // Send the Least Significant Byte
    byte error = Wire.endTransmission(); // Send the data and STOP condition

    if (error != 0) {
        Serial.print("!! I2C Write Error while writing to Register 0x");
        Serial.print(regAddr, HEX);
        Serial.print(". Error code: ");
        Serial.println(error);
        return false; // Indicate failure
    }
    return true; // Indicate success
}

// --- Helper Function: Read from a TMP102 Register ---
// Reads 2 bytes of data from the specified register address on the TMP102.
// Stores the data in 'dataBuffer' (MSB first).
// Returns true on success, false on I2C communication error.
bool readTmp102Register(uint8_t regAddr, uint8_t* dataBuffer) {
    // Step 1: Tell the TMP102 which register we want to read from
    Wire.beginTransmission(TMP102_ADDR);
    Wire.write(regAddr);
    // Send the request, but keep the connection open (repeated start)
    byte error = Wire.endTransmission(false);

    if (error != 0) {
        Serial.print("!! I2C Error while setting pointer to Register 0x");
        Serial.print(regAddr, HEX);
        Serial.print(" for reading. Error code: ");
        Serial.println(error);
        return false; // Indicate failure
    }

    // Step 2: Request the 2 bytes of data from the sensor
    uint8_t bytesRequested = 2;
    uint8_t bytesRead = Wire.requestFrom(TMP102_ADDR, bytesRequested);


    // Step 3: Check if we received the expected amount of data
    if (bytesRead == bytesRequested) {
        dataBuffer[0] = Wire.read(); // Read the Most Significant Byte
        dataBuffer[1] = Wire.read(); // Read the Least Significant Byte
        return true; // Indicate success
    } else {
        // Didn't get the expected 2 bytes
        Serial.print("!! I2C Read Error while reading from Register 0x");
        Serial.print(regAddr, HEX);
        Serial.print(". Expected ");
        Serial.print(bytesRequested);
        Serial.print(" bytes, but received ");
        Serial.println(bytesRead);
        return false; // Indicate failure
    }
}

// --- Helper Function: Convert Raw Temperature Data to Celsius ---
// Takes the 2-byte raw data from the TMP102 and converts it to degrees Celsius.
float temp_conv_C(const uint8_t* temp_raw) {
    // Combine the Most Significant Byte and Least Significant Byte into a 16-bit integer
    int16_t digital_temp = (int16_t)((temp_raw[0] << 8) | temp_raw[1]);

    // The TMP102 uses the top 12 bits for temperature data in normal mode (EM=0).
    // Shift right by 4 positions to align the data correctly.
    digital_temp = digital_temp >> 4;

    // Handle negative temperatures: If the sign bit (now the 12th bit) is set,
    // we need to extend the sign to the full 16 bits for correct negative representation.
    if (digital_temp & 0x0800) { // Check if the 12th bit is 1
            digital_temp |= 0xF000;  // Set the upper 4 bits to 1 (sign extension)
    }

    // Each LSB represents 0.0625 degrees Celsius.
    float temperature_c = (float)digital_temp * 0.0625f;

    return temperature_c;
}


// --- Arduino Setup Function (runs once at startup) ---
void setup() {
    // Start Serial communication for debugging output
    Serial.begin(115200);
    // Wait a moment for the serial monitor to connect (optional)
    delay(1000);
    Serial.println("\n--- TMP102 Temperature Alert System Initializing ---");
    Serial.println("----------------------------------------------------");

    // --- Configure Output Pins (Relays - Assumed Active HIGH) ---
    Serial.println("Setting up Relay Control Pins...");
    pinMode(RELAY_CH1_PIN, OUTPUT);
    pinMode(RELAY_CH2_PIN, OUTPUT);

    // Set initial level to HIGH to turn ON Active HIGH relays at startup
    digitalWrite(RELAY_CH1_PIN, HIGH);
    digitalWrite(RELAY_CH2_PIN, HIGH);
    relays_off_by_alert = false; // Relays start ON
    Serial.printf(" -> Relay Pins %d and %d configured as OUTPUT.\n", RELAY_CH1_PIN, RELAY_CH2_PIN);
    Serial.println(" -> Relays initially turned ON (assuming Active HIGH relays).");

    // --- Configure Component Enable Pin ---
    Serial.println("Setting up Component Enable Pin...");
    pinMode(ENABLE_PIN, OUTPUT);
    // Start with the pin LOW
    digitalWrite(ENABLE_PIN, LOW);
    Serial.printf(" -> Enable Pin %d configured as OUTPUT and set LOW.\n", ENABLE_PIN);
    // Wait briefly for power supply stabilization of external component
    Serial.println(" -> Delaying briefly for component power stabilization...");
    delay(100); // 100 millisecond delay
    // Set the pin HIGH to enable the component
    digitalWrite(ENABLE_PIN, HIGH);
    Serial.println(" -> Enable Pin set HIGH.");

    // --- Configure Input Pin and Interrupt (Alert) ---
    Serial.println("Setting up Temperature Alert Input Pin and Interrupt...");
    // The ALERT pin on the TMP102 is open-drain, so it needs a pull-up resistor.
    // We'll use the ESP32's internal pull-up.
    pinMode(ALERT_PIN, INPUT_PULLUP);

    // Attach the interrupt service routine (ISR) 'alertPinISR'.
    // Trigger ONLY on the FALLING edge (when the pin goes from HIGH to LOW).
    attachInterrupt(digitalPinToInterrupt(ALERT_PIN), alertPinISR, FALLING);
    Serial.printf(" -> Alert Pin %d configured as INPUT_PULLUP.\n", ALERT_PIN);
    Serial.println(" -> Interrupt attached to trigger on HIGH-to-LOW signal change.");

    // --- Initialize I2C Communication ---
    Serial.println("Initializing I2C communication...");
    Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
    Wire.setClock(I2C_FREQ_HZ); // Set the desired I2C speed
    Serial.printf(" -> I2C interface started. SDA=%d, SCL=%d, Frequency=%d Hz.\n", I2C_SDA_PIN, I2C_SCL_PIN, I2C_FREQ_HZ);

    // --- Configure TMP102 Sensor ---
    Serial.println("Configuring the TMP102 Temperature Sensor...");
    // Set Configuration Register (Address 0x01)
    // We want: Interrupt Mode (alert latches), Active LOW signal, 4 Faults to trigger, 4Hz update rate.
    uint16_t configValue = 0x7280; // TM=1, POL=0, F1=1, F0=0, CR1=1, CR0=0, EM=0
    Serial.printf(" -> Writing 0x%04X to CONFIG Register (0x01)...\n", configValue);
      if (!writeTmp102Register(POINTER_CONFIG, configValue)) {
            Serial.println("!! CRITICAL FAILURE: Could not configure TMP102. System Halted.");
            while(1) delay(100); // Stop execution
      }

    // Set TLOW Register (Address 0x02) - Low temperature threshold
    Serial.printf(" -> Writing 0x%04X to TLOW Register (0x02) for 90 degrees C...\n", TLOW_VALUE);
    if (!writeTmp102Register(POINTER_TLOW, TLOW_VALUE)) {
        Serial.println("!! CRITICAL FAILURE: Could not set TLOW threshold. System Halted.");
        while(1) delay(100); // Stop execution
    }

    // Set THIGH Register (Address 0x03) - High temperature threshold
    Serial.printf(" -> Writing 0x%04X to THIGH Register (0x03) for 120 degrees C...\n", THIGH_VALUE);
    if (!writeTmp102Register(POINTER_THIGH, THIGH_VALUE)) {
          Serial.println("!! CRITICAL FAILURE: Could not set THIGH threshold. System Halted.");
          while(1) delay(100); // Stop execution
    }

      Serial.println(" -> TMP102 Sensor Configuration Successful.");
      Serial.println("----------------------------------------------------");
      Serial.println("System Setup Complete. Starting main loop...");
      Serial.println("----------------------------------------------------");
}

// --- Arduino Loop Function (runs repeatedly) ---
void loop() {

    // Check if the alert flag was set by the ISR since the last check
    if (alert_occurred_flag) {
        Serial.println("\n>>> Temperature Alert Interrupt Triggered! <<<");

        // --- Handle the Alert Condition ---
        // Reset the flag immediately. Disable interrupts briefly to prevent
        // the ISR from modifying the flag while we check/reset it (atomic operation).
        noInterrupts();
        alert_occurred_flag = false;
        interrupts();
        Serial.println(" -> Alert flag cleared. Proceeding to check sensor.");

        // 1. Read the temperature register NOW.
        //    This is ESSENTIAL for two reasons in Interrupt Mode (TM=1):
        //    a) It clears the ALERT pin state on the TMP102, allowing it to go HIGH again later.
        //    b) It gets the current temperature so we can figure out WHY the alert happened.
        uint8_t tempRawDataAlert[2];
        Serial.print(" -> Reading Temperature Register (0x00) to clear alert & check cause...");
        if (readTmp102Register(POINTER_TEMP, tempRawDataAlert)) {
            // Successfully read temperature and cleared the sensor's alert condition.
            Serial.println(" Success.");

            // Convert to Celsius just for informative logging.
            float temp_c = temp_conv_C(tempRawDataAlert);
            Serial.printf("    -> Current Temperature: %.4f degrees C.\n", temp_c);

            // 2. Determine if the HIGH temperature threshold was the cause.
            //    Compare the raw 16-bit value read from the sensor.
            int16_t digital_temp_raw = (int16_t)((tempRawDataAlert[0] << 8) | tempRawDataAlert[1]);

            // Check if the temperature is at or above the high threshold setting.
            if (digital_temp_raw >= (int16_t)THIGH_VALUE) {
                  Serial.println(" -> Cause Identified: Temperature is at or above HIGH threshold (120 C).");
                  Serial.println(" -> ACTION: Turning OFF Relays.");
                  // Turn OFF the active-HIGH relays by setting pins LOW.
                  digitalWrite(RELAY_CH1_PIN, LOW);
                  digitalWrite(RELAY_CH2_PIN, LOW);
                  relays_off_by_alert = true; // Update state
            } else {
                  // If the temperature is now below THIGH, the alert was likely caused by:
                  // a) Temperature dropping below the LOW threshold (90 C).
                  // b) Temperature momentarily exceeding THIGH, triggering the interrupt,
                  //    but then dropping below THIGH before this code read the value.
                  // In either of these "non-high-temp" cases, we DO NOT turn off the relays.
                  Serial.println(" -> Cause Identified: Temperature is below HIGH threshold.");
                  Serial.println("    (Likely due to crossing TLOW or a brief THIGH spike).");
                  Serial.println(" -> ACTION: No change to relays.");
                  // Relays remain in their current state (which should be ON if not previously turned off).
            }
        } else {
            // This is a problem - we couldn't read the sensor after an alert!
            Serial.println("\n!! CRITICAL: Failed to read temperature after alert was detected!");
            Serial.println("   The alert state on the sensor might not be cleared.");
            // Consider adding more robust error handling here (e.g., retries, error state).
        }
          Serial.println(">>> Alert Handling Complete <<<");

    } // End of alert flag checking block


    // --- Regular Temperature Reading (Unconditional) ---
    // This happens every loop cycle regardless of alerts, for continuous monitoring.
    uint8_t tempRawDataRegular[2];
    // Serial.print("\nPerforming regular temperature check..."); // Less verbose logging option
    if (readTmp102Register(POINTER_TEMP, tempRawDataRegular)) {
        // Successfully read the current temperature.
        // Serial.println(" Success."); // Less verbose logging option
        float temp_c = temp_conv_C(tempRawDataRegular);
        Serial.printf("Current Temperature Reading: %.4f C\n", temp_c);

        // --- Optional: Logic to Turn Relays Back ON ---
        // If the relays were previously turned OFF by a high temp alert,
        // check if the temperature has fallen back to a safe level.
        if (relays_off_by_alert) {
                // Example: Turn back on if temp drops below 85 C (hysteresis below TLOW)
                float reset_threshold = 85.0;
                if (temp_c < reset_threshold) {
                        Serial.printf(" -> Temperature (%.2f C) is now well below threshold (< %.1f C).\n", temp_c, reset_threshold);
                        Serial.println(" -> ACTION: Turning Relays back ON.");
                        digitalWrite(RELAY_CH1_PIN, HIGH);
                        digitalWrite(RELAY_CH2_PIN, HIGH);
                        relays_off_by_alert = false; // Update state - relays are now ON
                } else {
                        // Temperature is still high, or hasn't dropped enough. Relays stay OFF.
                      // Serial.printf(" -> Temperature (%.2f C) still above reset threshold (%.1f C). Relays remain OFF.\n", temp_c, reset_threshold);
                }
        } else {
                // Relays are currently ON (or were never turned off).
                // You could add logic here if needed, e.g., ensuring they *are* HIGH.
                // Serial.println(" -> Relays are currently ON.");
        }

    } else {
        // Failed to read temperature during the regular check.
        Serial.println("!! Warning: Failed to read temperature during regular check.");
    }

    // --- Wait before next loop iteration ---
    // The delay() function on ESP32 (using FreeRTOS) allows background tasks
    // and interrupts (like our alert ISR) to occur while it waits.
    // It yields control to the scheduler, it does NOT block interrupts.
    // Serial.println("Waiting for next cycle..."); // Can be verbose
    delay(2000); // Wait for 2 seconds
}
