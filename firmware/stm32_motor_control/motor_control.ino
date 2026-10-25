// STM32 / Arduino C++ Firmware for Differential Track Actuation & PID Velocity Loop
#include <Servo.h>

// Pin definitions for L298N Motor Driver
const int ENA = 9;
const int IN1 = 8;
const int IN2 = 7;
const int ENB = 10;
const int IN3 = 6;
const int IN4 = 5;

void setup() {
    Serial.begin(115200);
    pinMode(ENA, OUTPUT);
    pinMode(ENB, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
}

void loop() {
    // Check for incoming velocity vectors from Jetson Orin Nano over UART
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        // Execute motor drive forward at PWM speed 200
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        analogWrite(ENA, 200);
        analogWrite(ENB, 200);
    }
    delay(10);
}