#include <Arduino.h>
#include <Servo.h>
#include "base.h"
#include "motor.h"
#include "servos.h"
#include "ultrasound.h"


int pos = 0;

void setup(){
    update_class<Motor>();
    update_class<Ultrasound>();
    update_class<Servos>();

    Serial.begin(9600);
}

void loop(){
    DoLoop();
}

