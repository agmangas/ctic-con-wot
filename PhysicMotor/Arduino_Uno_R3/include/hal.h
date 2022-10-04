/*
 * Header for the Hardware Abstraction Layer (HAL)
 * CTIC-WoT-CON - Kitten-killing machine
 * Components ports
 */

#ifndef HAL_H 
#define HAL_H

/* - - Includes - - */
#include <Arduino.h>


/* - - Defines - - */
#define MONITOR_SPEED 115200
#define MOTOR_PIN 2
#define BUTTON_PIN 3

/* - - Functions - - */
void InitSerialMonitor(bool is_debug=false);
void InitMotor();
void MotorOn();
void MotorOff();

void TestMotor(bool useButton = true);

//Button
void InitButton();
void WaitForButton(bool useKeyboard = true);

// Aux
void WaitForSeconds(unsigned int seconds);

#endif