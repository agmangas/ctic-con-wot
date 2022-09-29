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

// Settings
const bool ROTATE_BY_INTERVALS = true;
const bool IS_DEBUG = true;
const unsigned int INTERVAL_SECONDS = 540; // 9,5 minutes = 540 secs
const unsigned int ROTATION_SECONDS = 6;

// Functions
void setup()
{
  InitSerialMonitor(IS_DEBUG);
  InitMotor();
}

void loop()
{
  MotorOff();

  if (ROTATE_BY_INTERVALS)
  {
    WaitForSeconds(INTERVAL_SECONDS);
    MotorOn();
    WaitForSeconds(ROTATION_SECONDS);
  }
}