#include <Arduino.h>
#include <math.h>

double computeSum(String data) {
  double sum = 0.0;
  int pos = 0;
  while ((pos = data.indexOf(',')) != -1) {
    String numStr = data.substring(0, pos); // Extract number substring
    double num = numStr.toDouble(); // Convert substring to double
    sum += num; // Add number to sum
    data = data.substring(pos + 1); // Move to the next number
  }
  // Add the last number in the string
  sum += data.toDouble();
  return sum;
}

void setup() {
  Serial.begin(115200); // Start serial communication
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); // Read data from Python
    double sum = computeSum(data); // Compute the sum
    double sumSquared = pow(sum, 2); // Calculate sum squared
    double sqrtSum = sqrt(sum); // Calculate square root of sum

    // Send the results back to Python as comma-separated values
    Serial.print(sum);
    Serial.print(",");
    Serial.print(sumSquared);
    Serial.print(",");
    Serial.println(sqrtSum);
  }
}
