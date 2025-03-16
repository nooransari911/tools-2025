# Overview
The IR transmitter module reads and transmits height data. the IR receiver module receives the height and responds appropriately.

---
---

# Key considerations
## Power and cooling
IR LEDs and stepper motor need a lot of current. Power supply should be designed accordingly.

IR LEDs and stepper motors can get quite hot. Ensure proper cooling

## IR LEDs
TX and RX should have direct line-of-sight. LED should have enough power for the distance between TX and RX.

There must be reverse bias protection for IR LED.

IR LED drivers (dedicated ICs or MOSFETs) can be used for more robust performance.

MOSFET: low gate charge, low Vgsth

RX module should have sufficient sensitivity at the TX wavelength

IR LEDs can optionally be replaced with optical LEDs for higher data rate. RF can also be used for more range and more flexibility in environment.


## ToF sensor
ToF has been chosen over ultrasonic because it has better accuracy and is less sensitive to environment.


## IR Proximity sensor
Basic IR Proximity sensor. It can be replaced with cameras with image processing for more reliable detection of human presence
