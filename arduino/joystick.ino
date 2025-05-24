void setup() {
  Serial.begin(9600);

  pinMode(A0, INPUT); // Joystick X
  pinMode(A1, INPUT); // Joystick Y

  pinMode(2, INPUT_PULLUP); // Button 1 (DB15 Pin 2)
  pinMode(3, INPUT_PULLUP); // Button 2 (DB15 Pin 7)
}

int readStableAnalog(int pin) {
  analogRead(pin); delay(5);
  int total = 0;
  for (int i = 0; i < 4; i++) {
    total += analogRead(pin);
    delay(1);
  }
  return total / 4;
}

void loop() {
  int x = readStableAnalog(A0);
  int y = readStableAnalog(A1);

  bool button1 = !digitalRead(2); // true if pressed
  bool button2 = !digitalRead(3);

  Serial.print("X: "); Serial.print(x);
  Serial.print("  Y: "); Serial.print(y);
  Serial.print("  Btn1: "); Serial.print(button1 ? "PRESSED" : "off");
  Serial.print("  Btn2: "); Serial.println(button2 ? "PRESSED" : "off");

  delay(200);
}
