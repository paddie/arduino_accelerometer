const int groundpin = 18;             // analog input pin 4 -- ground
const int powerpin = 19;              // analog input pin 5 -- voltage
const int xpin = A3;                  // x-axis of the accelerometer
const int ypin = A2;                  // y-axis
const int zpin = A1;                  // z-axis (only on 3-axis models)

void setup()
{
  // initialize the serial communications:
  Serial.begin(9600);
  
  // Provide ground and power by using the analog inputs as normal
  // digital pins.  This makes it possible to directly connect the
  // breakout board to the Arduino.  If you use the normal 5V and
  // GND pins on the Arduino, you can remove these lines.
  pinMode(groundpin, OUTPUT);
  pinMode(powerpin, OUTPUT);
  digitalWrite(groundpin, LOW); 
  digitalWrite(powerpin, HIGH);
}

// int oldXval = 512;
// int oldDir = 512;

// const int deltaX = 50;

void loop() {
    // print the sensor values:
    
    // int xval = analogRead(xpin);
    // int dir = oldXval - xval;

    // Serial.print("old: ");
    // Serial.print(oldXval);
    // Serial.print(" - ");
    // Serial.print("new: ");
    // Serial.print(xval);
    // Serial.print(" (abs: ");
    // Serial.print(abs(oldXval - xval));
    // Serial.println(")");
    

    // if (abs(oldXval - xval) < deltaX) {
    //     oldXval = xval;
    //     // 512 - 300 = forward = +
    //     // 512 - 700 = backwards = -
    //     // 700 - 300 = forwards = +
    //     oldDir = oldXval - xval;
    //     delay(1000);

    //     return;
    // }

    // if (xval < 512) {
    //     Serial.print("+");
    //     if (xval < 300) {
    //         Serial.print("+");
    //     }
    //     Serial.println(xval);
    // } else {
    //     Serial.print("-");
    //     if (xval > 750) {
    //         Serial.print("-");
    //     }
    //     Serial.println(xval);
    // }

    // oldXval = xval;
    // oldDir = dir;

    Serial.print(analogRead(xpin));
    // print a tab between values:
    Serial.print("\t");
    Serial.print(analogRead(ypin));
    // print a tab between values:
    Serial.print("\t");
    Serial.print(analogRead(zpin));
    Serial.println();
    // delay before next reading:
    delay(100);
}
