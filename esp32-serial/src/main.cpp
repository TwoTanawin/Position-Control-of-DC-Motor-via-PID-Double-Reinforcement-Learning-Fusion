#include <Arduino.h>

int randomData1 = 0;
int randomData2 = 0;
int randomData3 = 0;

void setup() {
  Serial.begin(115200); // Start serial communication at 115200 baud rate
  randomSeed(analogRead(0)); // Seed the random number generator
}

void loop() {
    if (Serial.available() > 0) {
        // Read the incoming data
        char inputData[10];
        Serial.readBytesUntil('\n', inputData, 10);
        int inputNumber = atoi(inputData);

        // Increase the random values based on the input number
        randomData1 += inputNumber;
        randomData2 += inputNumber;
        randomData3 += inputNumber;

        // Send the updated random values back to Python
        Serial.print(randomData1);
        Serial.print(",");
        Serial.print(randomData2);
        Serial.print(",");
        Serial.println(randomData3);
    }
}
