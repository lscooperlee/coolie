#ifndef SERVOS_H
#define SERVOS_H

#include "base.h"
#include <Servo.h>

class Servos: public Base<'s'> {
    public:
        static Servos *GetInstance(){
            if(!instance)
                instance = new Servos();
            return instance;
        }

        void RunCmd(UartCmd &);

    private:
        static Servos *instance;

        Servos();

        Servo pitch;
        Servo yaw;
};

#endif
