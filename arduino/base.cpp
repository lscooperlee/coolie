#include "base.h"
#include <Arduino.h>


_Base *base_vector[128];

UartCmd UartWriteBuffer[8];
unsigned char UartWriteBufferIdx = 0;

UartCmd UartReadBuffer[8];
unsigned char UartReadBufferIdx = 0;

#define BUFSIZE(buf) (sizeof(buf)/sizeof(buf[0]))

void serialUp(int8_t cmd, int8_t subcmd, float p0, float p1, float p2, float p3){
    UartCmd uartcmd = {cmd, subcmd, p0, p1, p2, p3};
    serialPutWriteBuffer(uartcmd);
}

void serialDown(int8_t cmd, int8_t subcmd, float p0, float p1, float p2, float p3){
    UartCmd uartcmd = {cmd, subcmd, p0, p1, p2, p3};
    serialPutReadBuffer(uartcmd);
}

void serialPutWriteBuffer(UartCmd& cmd){
    noInterrupts();
    if(UartWriteBufferIdx < BUFSIZE(UartWriteBuffer))
        UartWriteBuffer[UartWriteBufferIdx++] = static_cast<UartCmd &&>(cmd);
    interrupts();
}

void serialPutReadBuffer(UartCmd& cmd){
    noInterrupts();
    if(UartReadBufferIdx < BUFSIZE(UartReadBuffer))
        UartReadBuffer[UartReadBufferIdx++] = static_cast<UartCmd &&>(cmd);
    interrupts();
}

void serialDoWriteBuffer(){
    noInterrupts();
    unsigned char tmpidx = UartWriteBufferIdx;
    UartCmd tmp[tmpidx];
    memcpy(tmp, UartWriteBuffer, sizeof(UartCmd) * UartWriteBufferIdx);
    UartWriteBufferIdx = 0;
    interrupts();

    while(tmpidx){
        Serial.write(reinterpret_cast<const char *>(&tmp[--tmpidx]), sizeof(UartCmd));
        Serial.flush();
    }
}

void serialDoReadBuffer(){
    noInterrupts();
    unsigned char tmpidx = UartReadBufferIdx;
    UartCmd tmp[BUFSIZE(UartReadBuffer)];
    memcpy(tmp, UartReadBuffer, sizeof(UartCmd) * UartReadBufferIdx);
    UartReadBufferIdx = 0;
    interrupts();

    while(tmpidx < BUFSIZE(UartReadBuffer)){
        if(Serial.available() >= static_cast<int>(sizeof(UartCmd))){
            char *cmdaddr = reinterpret_cast<char *>(&tmp[tmpidx++]);
            Serial.readBytes(cmdaddr, sizeof(UartCmd));    
        }else{
            break;
        }
    }

    while(tmpidx){
        auto m = base_vector[tmp[--tmpidx].cmd];
        if(m)
            m->RunCmd(tmp[tmpidx]);
    }

}

void DoLoop(){
    serialDoReadBuffer();
    serialDoWriteBuffer();
    for(auto b: base_vector){
        if(b)
            b->RunLoop();
    }
}

