/*
 * Header for the Hardware Abstraction Layer (HAL)
 * CTIC-WoT-CON - Kitten-killing machine
 * Components ports
 */

#ifndef HAL_H 
#define HAL_H

/* - - Includes - - */
#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>


/* - - Defines - - */
#define MONITOR_SPEED 115200
#define MOTOR_PIN 2
#define BUTTON_PIN 3

//If use Heltec WiFi LoRa 32
#define OLED_SDA 4
#define OLED_SCL 15 
#define OLED_RST 16
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define INIT_DISPLAY_COLUMN 0
#define FIRST_DISPLAY_ROW 10
#define SECOND_DISPLAY_ROW 20
#define THIRD_DISPLAY_ROW 30
#define FOURTH_DISPLAY_ROW 40
#define FIFTH_DISPLAY_ROW 50

/* - - Functions - - */
void InitSerialMonitor(bool is_debug=false);
void InitMotor();

//Motor
void MotorOn(bool useScreen = false);
void MotorOff(bool useScreen = false);

void TestMotor(bool useButton = true);

//Button
void InitButton();
void WaitForButton(bool useKeyboard = true);

// Screen
void InitDisplay();
void WriteInDisplay(String message, bool clean=true, int row=INIT_DISPLAY_COLUMN, int column=INIT_DISPLAY_COLUMN);
void ClearDisplay();

// Aux
void WaitForSeconds(unsigned int seconds, bool useScreen = false);

#endif