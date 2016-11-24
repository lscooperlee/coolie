
#include "ultrasound.h"

#include <PulseInZero.h>


Ultrasound *Ultrasound::instance = nullptr;

static constexpr float SpeedOfSound     	= 343.2; // ~speed of sound (m/s) in air, at 20°C         
static constexpr float MicrosecondsPerMillimetre 	= 1000.0 / SpeedOfSound; // microseconds per millimetre - sound travels 1 mm in ~2.9us
static constexpr float  MicrosecondsToMillimetres  = (1.0 / MicrosecondsPerMillimetre);
static constexpr float  MicrosecondsToMillimetres2 = MicrosecondsToMillimetres / 2.0; // beam travels the distance twice... so halve the time.
static constexpr int SIGNAL_PIN = 6;

unsigned long lastTime= 0;
int pingTimer= 0;
int pingDelay= 500; // milliseconds between ping pulses
float millimetres = 0.0;


unsigned int threshold = 350;
bool isThresholdTriggered = false;

void pingPulseComplete(unsigned long duration) {

    millimetres = MicrosecondsToMillimetres2 * duration;

    if (millimetres > 4000) {
        millimetres = 4000;
    }

    if (millimetres < threshold) {
        if (isThresholdTriggered == false) {
            isThresholdTriggered = true;

            serialDown('m', 'n');
            serialUp('u', 'e', millimetres);

        }
    } else {
        isThresholdTriggered = false;
    }

}

Ultrasound::Ultrasound():Base()
{
  pinMode(SIGNAL_PIN, OUTPUT);
  digitalWrite(SIGNAL_PIN, LOW); 
	
  PulseInZero::setup(pingPulseComplete);
}

void Ultrasound::RunLoop() {
  
  unsigned long time = millis();
  unsigned long dt   = time - lastTime;
  lastTime = time;
  
  pingTimer += dt;
  if(pingTimer > pingDelay){  
	pingTimer = 0;
	ping();
  }

  
}

void Ultrasound::ping(){

  digitalWrite(SIGNAL_PIN, HIGH);
  delayMicroseconds(10); 
  digitalWrite(SIGNAL_PIN, LOW);
  
  PulseInZero::begin();
}

void Ultrasound::RunCmd(UartCmd &cmd){
    serialUp('u', 'u', millimetres, 0, 0, 0);
}
