/*
 * Hardware Abstraction Layer (HAL)
 * CTIC-WoT-CON - Kitten-killing machine
 * Implementation
 */

#include "hal.h"

/** Functions **/
void InitSerialMonitor(bool is_debug)
{
    Serial.begin(MONITOR_SPEED);
    while (is_debug && !Serial) ;
}

//MOTOR

void InitMotor(){
    pinMode(MOTOR_PIN_OUT, OUTPUT);
}

void MotorOn(){
    Serial.println("--> Motor on");
    digitalWrite(MOTOR_PIN_OUT, LOW); // For some reason, it is inverted (On = Low)
}

void MotorOff(){
    Serial.println("--> Motor off");
    digitalWrite(MOTOR_PIN_OUT, HIGH); // For some reason, it is inverted (Off = High)
}

//Aux

void WaitForSeconds(int seconds){
    Serial.print("--> Waiting for ");
    Serial.print(seconds);
    Serial.println(" seconds . . .\n");
    delay(seconds * 1000);
}