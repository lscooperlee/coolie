#ifndef MOTOR_H
#define MOTOR_H

#include "base.h"

class Motor: public Base<'m'> {
    public:
        static Motor *GetInstance(){
            if(!instance)
                instance = new Motor();
            return instance;
        }

        void RunCmd(UartCmd &) override;
        void RunLoop() override;

    private:
        static Motor *instance;
        uint8_t percent = 5;

        static void leftCountOne();

        static void rightCountOne();

        Motor();

        void init();

        void forward(float speed, float distance);

        void backward(float speed, float distance);

        void turnleft(float speed, float angle);

        void turnright(float speed, float angle);

        void setSpeed(float);

        void setDistance(float, int8_t leftDir, int8_t rightDir);

        void setAngle(float, int8_t leftDir, int8_t rightDir);

        void stop();
};

#endif
