#include <Arduino.h>

/*********************RIGHT wheel variables*****************************/
#define PWM_R 9
#define inA_R 10
#define inB_R 11

#define ENCA_R 2
#define ENCB_R 3
volatile long encoderPos_R = 0;
volatile long targetPos_R = 0;

// PID variables
double kp = 1.0;
double ki = 0.0;
double kd = 0.0;
double prevError = 0.0;
double integral = 0.0;

double calculatePID(double currentPos) {
  double error = targetPos_R - currentPos;
  integral += error;
  double derivative = error - prevError;
  double output = kp * error + ki * integral + kd * derivative;
  prevError = error;
  return output;
}

/*
   Encoder motor right
*/
void readEncoder_R() {               /*pulse and direction, direct port reading to save cycles*/
  int b = digitalRead(ENCB_R);
  if (b > 0) {                       /*if b > 0   count ++;*/
    encoderPos_R++;
  }
  else {
    encoderPos_R--;                   /*if b < 0   count --;*/
  }
}

// /**********************Motor RIGHT direction**********************/
void pwmOut_R(int out) {
  if (out > 0) {
    analogWrite(PWM_R, out);                  /*drive motor right CW*/
    digitalWrite(inA_R, HIGH);
    digitalWrite(inB_R, LOW);
  }
  else {
    analogWrite(PWM_R, abs(out));             /*drive motor right CCW*/
    digitalWrite(inA_R, LOW);
    digitalWrite(inB_R, HIGH);
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(PWM_R, OUTPUT);
  pinMode(inA_R, OUTPUT);
  pinMode(inB_R, OUTPUT);

  pinMode(ENCA_R, INPUT);
  pinMode(ENCB_R, INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA_R), readEncoder_R, RISING);
}

void loop() {
  // put your main code here, to run repeatedly:
  targetPos_R = 90; // Set the target position (360 pulses)

  long currentPos = encoderPos_R;
  double output = calculatePID(currentPos);
  pwmOut_R(output);

  Serial.print("Target Position: ");
  Serial.print(targetPos_R);
  Serial.print(" Current Position: ");
  Serial.print(currentPos);
  Serial.print(" Output: ");
  Serial.println(output);

  delay(100); // Adjust delay as needed
}
