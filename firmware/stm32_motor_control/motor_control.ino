/* 
 * Production Embedded Firmware: Closed-Loop PID Velocity Control & Differential Drive
 * Autonomous Sub-Surface Resonance Rover - Physical AI Track
 */

#include <util/atomic.h>

// Pin Mappings for Encoder and L298N Driver
const int ENC_A_LEFT = 2;
const int ENC_B_LEFT = 3;
const int PWM_LEFT = 9;
const int DIR_LEFT_1 = 8;
const int DIR_LEFT_2 = 7;

// Volatile variables updated by hardware ISRs
volatile long left_encoder_count = 0;
unsigned long previous_millis = 0;
float target_velocity = 0.0;
float current_velocity = 0.0;

// PID Tuning Parameters
float kp = 1.25, ki = 0.08, kd = 0.02;
float error = 0, previous_error = 0, integral = 0, derivative = 0;

void setup() {
    Serial.begin(230400); // High-speed telemetry and command link
    pinMode(PWM_LEFT, OUTPUT);
    pinMode(DIR_LEFT_1, OUTPUT);
    pinMode(DIR_LEFT_2, OUTPUT);
    pinMode(ENC_A_LEFT, INPUT_PULLUP);
    pinMode(ENC_B_LEFT, INPUT_PULLUP);

    attachInterrupt(digitalPinToInterrupt(ENC_A_LEFT), handleEncoderLeft, RISING);
}

void loop() {
    unsigned long current_millis = millis();
    if (current_millis - previous_millis >= 10) { // Exact 100 Hz execution loop
        previous_millis = current_millis;

        long enc_counts;
        ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
            enc_counts = left_encoder_count;
            left_encoder_count = 0; // Reset delta accumulator
        }

        // Calculate velocity feedback
        current_velocity = (enc_counts * 100.0) / 540.0;

        // Compute PID Error Correction
        error = target_velocity - current_velocity;
        integral += error * 0.01;
        derivative = (error - previous_error) / 0.01;
        float pid_output = (kp * error) + (ki * integral) + (kd * derivative);
        previous_error = error;

        int pwm_output = constrain((int)(abs(pid_output) * 50.0), 0, 255);
        driveMotor(pwm_output, pid_output >= 0);
    }

    // Ingest streaming velocity vectors from Jetson Orin Nano
    if (Serial.available() > 0) {
        target_velocity = Serial.parseFloat();
    }
}

void handleEncoderLeft() {
    if (digitalRead(ENC_B_LEFT) == HIGH) {
        left_encoder_count++;
    } else {
        left_encoder_count--;
    }
}

void driveMotor(int pwm, boolean forward) {
    analogWrite(PWM_LEFT, pwm);
    digitalWrite(DIR_LEFT_1, forward ? HIGH : LOW);
    digitalWrite(DIR_LEFT_2, forward ? LOW : HIGH);
}