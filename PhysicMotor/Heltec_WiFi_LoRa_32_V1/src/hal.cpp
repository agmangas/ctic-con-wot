/*
 * Hardware Abstraction Layer (HAL)
 * CTIC-WoT-CON - Kitten-killing machine
 * Implementation
 */

#include "hal.h"

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RST);

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

void MotorOn(bool useScreen)
{
    Serial.println("--> Motor on");
    digitalWrite(MOTOR_PIN, LOW); // For some reason, it is inverted (On = Low)

    if(useScreen)
        WriteInDisplay("Motor ON!");
}

void MotorOff(bool useScreen)
{
    Serial.println("--> Motor off");
    digitalWrite(MOTOR_PIN, HIGH); // For some reason, it is inverted (Off = High)

    if(useScreen)
        WriteInDisplay("Motor OFF :(");
}

void TestMotor(bool useButton)
{
    Serial.println("############ STARTING TESTING PHASE . . . ############");
    if (useButton)
        WaitForButton();
    MotorOn();
    WaitForSeconds(1);
    MotorOff();
    Serial.println("############ . . . TESTING PHASE FINISHED ############");
    return;
}

// BUTTON
void InitButton()
{
    pinMode(BUTTON_PIN, INPUT);
}

void WaitForButton(bool useKeyboard)
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

// Screen
void InitDisplay()
{
    // reset OLED display via software
    pinMode(OLED_RST, OUTPUT);
    digitalWrite(OLED_RST, LOW);
    delay(20);
    digitalWrite(OLED_RST, HIGH);

    // initialize OLED
    Wire.begin(OLED_SDA, OLED_SCL);
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3c, false, false))
    { // Address 0x3C for 128x32
        Serial.println(F("SSD1306 allocation failed"));
        for (;;)
            ; // Don't proceed, loop forever
    }

    Serial.println("INIT DISPLAY");
    WriteInDisplay("DISPLAY OK");
    display.clearDisplay();
    display.setTextColor(WHITE);
    display.setTextSize(1);
    display.display();
}

void WriteInDisplay(String message, bool clean, int row, int column)
{
    if(clean)
        ClearDisplay();
    display.setCursor(column, row);

    display.print(message);
    display.display();
}

void ClearDisplay()
{
    display.clearDisplay();
    display.display();
}

// Aux

void WaitForSeconds(unsigned int seconds, bool useScreen)
{
    Serial.print("--> Waiting for ");
    Serial.print(seconds);
    Serial.println(" seconds . . .");

    unsigned long msTotal = seconds * long(1000);
    unsigned long startMillis = millis();

    long currentSecs = 0;
    char temp_string[20];

    unsigned long msCurrent = millis();
    while (msCurrent - startMillis < msTotal)
        if ((msCurrent - startMillis) % 10000 == 0)
        { // One print per 10 seconds
            Serial.print(".");
            if (useScreen)
            {
                WriteInDisplay("Waiting . . .");
                currentSecs = (msTotal - (msCurrent-startMillis))/1000;            
                sprintf(temp_string, "- Total: %d s", seconds); 
                WriteInDisplay(temp_string, false, SECOND_DISPLAY_ROW);
                sprintf(temp_string, "- Remaining: %d s", currentSecs); 
                WriteInDisplay(temp_string, false, THIRD_DISPLAY_ROW);
            }
        }

        msCurrent = millis();
}