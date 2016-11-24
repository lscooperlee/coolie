#ifndef BASE_H
#define BASE_H

#include <Arduino.h>

struct UartCmd {
    int8_t cmd;
    int8_t subcmd;
    float param0;
    float param1;
    float param2;
    float param3;
};

class _Base {
    public:
        virtual void RunCmd(UartCmd &cmd){}
        virtual void RunLoop(){};
};

template <int N>
class Base : public _Base {
    public:
        static constexpr int CMD = N;
};

extern _Base *base_vector[128];

template <typename type>
void update_class(void){
    base_vector[type::CMD] = type::GetInstance();
}

void serialPutWriteBuffer(UartCmd& cmd);
void serialPutReadBuffer(UartCmd& cmd);
void serialUp(int8_t cmd, int8_t subcmd, float p0 = 0, float p1 = 0, float p2 = 0, float p3 = 0);
void serialDown(int8_t cmd, int8_t subcmd, float p0 = 0, float p1 = 0, float p2 = 0, float p3 = 0);
void DoLoop();

#endif
