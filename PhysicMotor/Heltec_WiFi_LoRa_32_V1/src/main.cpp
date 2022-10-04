//==========================================================================================================
//████████╗██╗  ██╗███████╗    ██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗
//╚══██╔══╝██║  ██║██╔════╝    ██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
//   ██║   ███████║█████╗      ██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗
//   ██║   ██╔══██║██╔══╝      ██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝
//   ██║   ██║  ██║███████╗    ╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
//   ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
//
//██╗  ██╗██╗████████╗████████╗███████╗███╗   ██╗      ██╗  ██╗██╗██╗     ██╗     ██╗███╗   ██╗ ██████╗
//██║ ██╔╝██║╚══██╔══╝╚══██╔══╝██╔════╝████╗  ██║      ██║ ██╔╝██║██║     ██║     ██║████╗  ██║██╔════╝
//█████╔╝ ██║   ██║      ██║   █████╗  ██╔██╗ ██║█████╗█████╔╝ ██║██║     ██║     ██║██╔██╗ ██║██║  ███╗
//██╔═██╗ ██║   ██║      ██║   ██╔══╝  ██║╚██╗██║╚════╝██╔═██╗ ██║██║     ██║     ██║██║╚██╗██║██║   ██║
//██║  ██╗██║   ██║      ██║   ███████╗██║ ╚████║      ██║  ██╗██║███████╗███████╗██║██║ ╚████║╚██████╔╝
//╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═══╝      ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝
//
//███╗   ███╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗███████╗
//████╗ ████║██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝
//██╔████╔██║███████║██║     ███████║██║██╔██╗ ██║█████╗
//██║╚██╔╝██║██╔══██║██║     ██╔══██║██║██║╚██╗██║██╔══╝
//██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║██║ ╚████║███████╗
//╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
//                                                                        By CTIC-Wot.
//==========================================================================================================

#include <Arduino.h>
#include <hal.h>
#include "mqttClient.h"

// Settings
const bool ROTATE_BY_INTERVALS = true; // Put inf false and will rotate forever
const bool IS_DEBUG = true;
const unsigned int INTERVAL_SECONDS = 570; // 9,5 minutes = 570 secs
const unsigned int ROTATION_SECONDS = 10;

const bool USE_BUTTON = false;
const bool EXECUTE_TESTING = true;

const bool USE_DISPLAY = true;

// Functions
void setup()
{
  InitSerialMonitor(IS_DEBUG);
  InitMotor();
  InitButton();
  InitWifi();
  ConnectMQTT();

  if(USE_DISPLAY)
    InitDisplay();

  if (EXECUTE_TESTING)
    TestMotor(USE_BUTTON);
  if (!ROTATE_BY_INTERVALS)
    MotorOn(USE_DISPLAY);
}

void loop()
{
  if (ROTATE_BY_INTERVALS)
  {
    MotorOff(USE_DISPLAY);
    
    if (USE_BUTTON)
      WaitForButton(true);

    WaitForSeconds(INTERVAL_SECONDS, USE_DISPLAY);
    MotorOn(USE_DISPLAY);
    WaitForSeconds(ROTATION_SECONDS, USE_DISPLAY);
  }
}