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
    while (is_debug && !Serial)
        ;
}

// MOTOR

void InitMotor()
{
    pinMode(MOTOR_PIN, OUTPUT);
    MotorOff();
}

void InitButton()
{
    pinMode(BUTTON_PIN, INPUT);
}

void MotorOn()
{
    Serial.println("--> Motor on");
    digitalWrite(MOTOR_PIN, LOW); // For some reason, it is inverted (On = Low)
}

void MotorOff()
{
    Serial.println("--> Motor off");
    digitalWrite(MOTOR_PIN, HIGH); // For some reason, it is inverted (Off = High)
}

void TestMotor(bool useButton = true)
{
    Serial.println("############ STARTING TESTING PHASE . . . ############");
    if(useButton)
        WaitForButton();
    MotorOn();
    WaitForSeconds(1);
    MotorOff();
    Serial.println("############ . . . TESTING PHASE FINISHED ############");
    return;
}

// BUTTON
void WaitForButton(bool useKeyboard = true)
{
    Serial.print("--> Waiting for button . . .");
    int buttonState = 0;
    while (buttonState != HIGH || (useKeyboard && Serial.available() < 1))
    {
        if (useKeyboard)
            Serial.read();
        buttonState = digitalRead(BUTTON_PIN);
    }
    Serial.println(" BUTTON PRESSED !!!!");
}
// Aux

void WaitForSeconds(unsigned int seconds)
{    
    Serial.print("--> Waiting for ");
    Serial.print(seconds);
    Serial.println(" seconds . . .");

    unsigned long ms = seconds*long(1000);
    unsigned long startMillis = millis();
    
    while (millis() - startMillis < ms)
        if ((millis() - startMillis) % 10000 == 0) // One print per 10 seconds
            Serial.print(".");
        
}