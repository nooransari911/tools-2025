#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 or the address of your LCD
// You can find the address by using I2C scanner code
#define LCD_ADDRESS 0x27
#define LCD_COLS 16
#define LCD_ROWS 2

LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_COLS, LCD_ROWS);

void setup() {
  // Initialize the LCD
  lcd.init();
  // Turn on the backlight
  lcd.backlight();
  // Print "Hello World" on the LCD
  

}

void loop() {
  int smoke = analogRead (A0);
  lcd.setCursor(0, 0);
  lcd.print("Smoke value:");
  lcd.print (smoke);
  delay (500);

  /*
  lcd.setCursor(0, 1);
  lcd.print("Temp:28C");
  delay (1000);
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Pres:1007mbar");
  lcd.setCursor(0, 1);
  lcd.print("Rain:0");
  delay (1000);
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Humi:36%");
  delay (1000);
  */
  lcd.clear();
}
