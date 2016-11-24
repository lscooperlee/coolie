
#include "servos.h"

constexpr int pitch_pin = 10u;
constexpr int yaw_pin = 9u;

void Servos::RunCmd(UartCmd &cmd){
    int angle = cmd.param0;

    if(angle > 180 )
        angle = 180;
    else if(angle < 0)
        angle = 0;

    switch(cmd.subcmd){
        case 'p':
            pitch.write(angle);
            break;
        case 'y':
            yaw.write(angle);
            break;
    }
}

Servos *Servos::instance = nullptr;

Servos::Servos():
    pitch(),
    yaw()
{
    pitch.attach(pitch_pin);
    pinMode(pitch_pin, OUTPUT);

    yaw.attach(yaw_pin);
    pinMode(yaw_pin, OUTPUT);
}
