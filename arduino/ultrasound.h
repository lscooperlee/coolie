#ifndef ULTRASOUND_H
#define ULTRASOUND_H

#include "base.h"

class Ultrasound: public Base<'u'> {
    public:
        static Ultrasound *GetInstance(){
            if(!instance)
                instance = new Ultrasound();
            return instance;
        }

        void RunCmd(UartCmd &cmd) override;
        void RunLoop() override;

    private:
        static Ultrasound *instance;

        Ultrasound();

        void ping();

};


#endif
