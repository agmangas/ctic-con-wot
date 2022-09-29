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
#define MOTOR_PIN_OUT 2

/* - - Functions - - */
void InitSerialMonitor(bool is_debug=false);
void InitMotor();
void MotorOn();
void MotorOff();
void WaitForSeconds(int seconds);
#endif