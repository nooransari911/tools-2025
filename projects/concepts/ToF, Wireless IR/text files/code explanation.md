# Code Brief
## System 1
- Setup Function:
    - Initializes the IR proximity sensor, IR transmitter, and VL53L0X sensor.
    - Configures pin modes for sensor inputs and outputs.

- Loop Function:
    - Continuously check for human presence.
    - If presence is detected, it measures the height and transmits it over IR transmitter if the height is greater than zero.

- Sensor Height Function:
    - Measures height from VL53L0X sensor
    - Constrains the height value to a maximum of 255 and checks for timeouts.
    - Returns height value to loop


## System 2
- Setup Function:
    - Initializes the IR receiver and sets up pin modes for the stepper motor

- Loop Function:
    - Listens for incoming IR signals.
    - If a signal is received and is valid, it extracts the height value.
    - If the height exceeds 1000 mm, it calls the `stepper_action()` function.

- Stepper Action Function:
    - Activates the stepper motor to rotate based on the received height.
    - Controls the direction and steps for the motor.

---
---
