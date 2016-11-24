#include <Arduino.h>
#include "motor.h"
#include "PinChangeInt.h"

#define MOTOR_LEFT_IN2       4
#define MOTOR_LEFT_IN1       5
#define MOTOR_LEFT_ENA       3

#define MOTOR_RIGHT_IN2      12
#define MOTOR_RIGHT_IN1      13
#define MOTOR_RIGHT_ENA      11

#define MOTOR_LEFT_COUNT1     A0
#define MOTOR_LEFT_COUNT2     A1
#define MOTOR_RIGHT_COUNT1    A2
#define MOTOR_RIGHT_COUNT2    A3

int8_t leftDir = 0;
int8_t rightDir = 0;

int32_t leftCounter1 = 0;
int32_t leftCounter2 = 0;

int32_t rightCounter1 = 0;
int32_t rightCounter2 = 0;

int32_t lastLeftCounter1 = 0;
int32_t lastRightCounter1 = 0;

int32_t expectedLeftCounter = 0;
int32_t expectedRightCounter = 0;

bool noStop = true;

float distanceRatio = 4.8;      // count per cm
constexpr int8_t Radius = 12;  //cm

Motor *Motor::instance = nullptr;

void Motor::leftCountOne(){
    if(leftDir > 0)
        leftCounter1++;
    else if(leftDir < 0)
        leftCounter1--;

    if(!noStop && expectedLeftCounter == leftCounter1){
        instance->stop();

        serialUp('m', 'e');
    }
}  

void Motor::rightCountOne(){
    if(rightDir > 0)
        rightCounter1++;
    else if(rightDir < 0)
        rightCounter1--;

    if(!noStop && expectedRightCounter == rightCounter1){
        instance->stop();

        serialUp('m', 'e');
    }
}  

Motor::Motor():Base(),percent(5){
    init();
    stop();

    attachPinChangeInterrupt(MOTOR_LEFT_COUNT1, Motor::leftCountOne, RISING);
    attachPinChangeInterrupt(MOTOR_RIGHT_COUNT1, Motor::rightCountOne, RISING);
}

void Motor::RunCmd(UartCmd &cmd){
    switch(cmd.subcmd){
        case 'w':
            forward(cmd.param0, cmd.param1);
            break;
        case 'a':
            turnleft(cmd.param0, cmd.param1);
            break;
        case 'd':
            turnright(cmd.param0, cmd.param1);
            break;
        case 's':
            backward(cmd.param0, cmd.param1);
            break;
        case 'n':
            stop();
            break;
        case 'u':
            setSpeed(cmd.param0);
            break;
        case 'c':
            serialUp('m', 'c', leftCounter1, rightCounter1);
            break;
    }
}

void Motor::init(){
    pinMode(MOTOR_LEFT_IN2, OUTPUT);
    pinMode(MOTOR_LEFT_IN1, OUTPUT);

    pinMode(MOTOR_RIGHT_IN2, OUTPUT);
    pinMode(MOTOR_RIGHT_IN1, OUTPUT);
}

void Motor::forward(float speed, float distance){

    setSpeed(speed);
    setDistance(distance, 1, 1);

    digitalWrite(MOTOR_RIGHT_IN1, HIGH);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);

    digitalWrite(MOTOR_LEFT_IN1, HIGH);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
}

void Motor::backward(float speed, float distance){

    setSpeed(speed);
    setDistance(distance, -1, -1);

    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, HIGH);

    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, HIGH);
}

void Motor::turnright(float speed, float angle){

    setSpeed(speed);
    setAngle(angle, 1, -1);

    digitalWrite(MOTOR_RIGHT_IN1, HIGH);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);

    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, HIGH);
}

void Motor::turnleft(float speed, float angle){

    setSpeed(speed);
    setAngle(angle, -1, 1);

    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, HIGH);

    digitalWrite(MOTOR_LEFT_IN1, HIGH);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
}

void Motor::setDistance(float p, int8_t leftDir, int8_t rightDir){
    if(p > 0.1) {
        noStop = false;
        int32_t distCount = p * distanceRatio;
        expectedRightCounter = distCount * rightDir + rightCounter1;
        expectedLeftCounter = distCount * leftDir + leftCounter1;
    } else {
        noStop = true;
    }
}

void Motor::setAngle(float p, int8_t leftDir, int8_t rightDir){
    if(p > 0.1) {
        noStop = false;
        int32_t angleCount = p * distanceRatio * Radius;
        expectedRightCounter = angleCount * rightDir + rightCounter1;
        expectedLeftCounter = angleCount * leftDir + leftCounter1;
    } else {
        noStop = true;
    }
}

void Motor::setSpeed(float p){
    if(p > 0 && p <= 10)
        percent = p;
    
    pinMode(MOTOR_LEFT_ENA, OUTPUT);
    pinMode(MOTOR_RIGHT_ENA, OUTPUT);
    
    TCCR2A = _BV(COM2A1) | _BV(COM2B1) | _BV(WGM21) | _BV(WGM20);
    TCCR2B = _BV(CS22);
    OCR2A = percent * 15 + 100;
    OCR2B = percent * 15 + 100;
    
}

void Motor::stop(){
    leftDir = 0;
    rightDir = 0;

    digitalWrite(MOTOR_LEFT_ENA, LOW);
    digitalWrite(MOTOR_RIGHT_ENA, LOW);

    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);

    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
}

static int8_t runLoopCount = 0; 
void Motor::RunLoop() {
    runLoopCount = (1 + runLoopCount) % 50;
    if(runLoopCount == 0){

        if(leftDir != 0){
            int32_t d = lastLeftCounter1 - leftCounter1;
            if(abs(d) < 5){
                serialUp('w', 'k');
            }
        }

        if(rightDir != 0){
            int32_t d = lastRightCounter1- rightCounter1;
            if(abs(d) < 5){
                serialUp('w', 'k');
            }
        }

        lastRightCounter1 = rightCounter1;
        lastLeftCounter1 = leftCounter1;
    }
}
