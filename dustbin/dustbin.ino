#include <Servo.h>

Servo motor1;
Servo motor2;

void setup() {
  motor1.attach(9);  // Motor 1 to pin 9
  motor2.attach(10); // Motor 2 to pin 10
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    if (command == 'O') {
      // Organic: Motor1 Right
      motor1.write(120);
      motor2.write(90);
    }
    else if (command == 'P') {
      // Plastic: Motor1 Left + Motor2 Left
      motor1.write(60);
      motor2.write(60);
    }
    else if (command == 'M') {
      // Metal: Motor1 Left + Motor2 Right
      motor1.write(60);
      motor2.write(120);
    }

    delay(2000); // Hold position
    motor1.write(90); // Reset position
    motor2.write(90); // Reset position
  }
}
