// ConstantSpeed.pde
// -*- mode: C++ -*-
//
// Shows how to run AccelStepper in the simplest,
// fixed speed mode with no accelerations
// Requires the Adafruit_Motorshield v2 library 
//   https://github.com/adafruit/Adafruit_Motor_Shield_V2_Library
// And AccelStepper with AFMotor support 
//   https://github.com/adafruit/AccelStepper

// This tutorial is for Adafruit Motorshield v2 only!
// Will not work with v1 shields

#include <Wire.h>
#include <AccelStepper.h>
#include <Adafruit_MotorShield.h>

long int newPos = 0;
bool newMove = false;
// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myStepper1 = AFMS.getStepper(200, 2);

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
void forwardstep1() {  
  myStepper1->onestep(FORWARD, MICROSTEP);
}
void backwardstep1() {  
  myStepper1->onestep(BACKWARD, MICROSTEP);
}

AccelStepper Astepper1(forwardstep1, backwardstep1); // use functions to step

void setup()
{  
   Serial.begin(9600);           // set up Serial library at 9600 bps
   Serial.println("Stepper test!");
  
  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz

  Astepper1.setSpeed(50);	
  Astepper1.currentPosition();
}

void loop()
{  
   //Astepper1.runSpeed();
//  Astepper1.runToNewPosition(500);
//  Astepper1.runToPosition();

  if(newMove){
    Astepper1.runToNewPosition(newPos);
    Astepper1.runToPosition();
    newMove = false;
    Serial.print(" Move Complete. Now at: ");
    Serial.println(newPos);
  }



/*  
  Astepper1.runToNewPosition(0);
  Astepper1.runToPosition();
  Astepper1.runToNewPosition(500);
  Astepper1.runToPosition();
  Astepper1.runToNewPosition(0);
  Astepper1.runToPosition();
*/
//   while(1);
}

void serialEvent(){
  newMove = true;
  newPos = Serial.parseInt();
  Serial.read();
  Serial.print(" Moving to: ");
  Serial.println( newPos );
}

