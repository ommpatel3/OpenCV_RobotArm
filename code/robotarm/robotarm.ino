#include <Wire.h>
#include <Servo.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_FREQ 50
Servo claw;

//setting servo min/max PWM values
#define BIGSERVOMIN  110
#define BIGSERVOMAX  420 
#define SMLSERVOMIN  70
#define SMLSERVOMAX  430

//declare servo channels on PCA9685
#define ARM1PIN  4
#define ARM2PIN  12 
#define ROTATIONPIN  8
#define CLAWPIN  0

//declare servo movement ranges, used for representing positions as percent
const int rangeArm1[]={180, 120};
const int rangeArm2[]={140, 185};
const int rangeRotation[]={45, 135};

//storing current position
int arm1Pos = 0;
int arm2Pos = 0;
int rotationPos = 50;
int clawPos = 180;

//storing target position
int arm1Tgt = 0;
int arm2Tgt = 0;
int rotationTgt = 50;
int clawTgt = 180;

String input;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(50);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);

  claw.attach(9);

  delay(10);  
}

void loop() {

  input = Serial.readStringUntil('\r');
  
  if (!input.equals("")){
    Serial.println(input);
    arm1Tgt = input.substring(0,3).toInt();
    rotationTgt = input.substring(3,6).toInt();
    arm2Tgt = input.substring(6,9).toInt();
  }

    //claw control
  if (input.substring(9,10).toInt() == 2){
    clawTgt = 180;
  }
  else if (input.substring(9,10).toInt() == 1){
    clawTgt = 120;
  }

  updatePos(arm1Tgt, arm1Pos);
  updatePos(arm2Tgt, arm2Pos);
  updatePos(rotationTgt, rotationPos);
  updatePos(clawTgt,clawPos);

  //sending current positions
  servoPercent(ARM1PIN,arm1Pos);
  servoPercent(ARM2PIN,arm2Pos);
  servoPercent(ROTATIONPIN,rotationPos);
  claw.write(clawPos);

  //delay (10);


}
//#######################################################################################################
//converts percent movement -> angle ->PWM to motor

void updatePos(int tgt, int & pos){
  if (tgt > 100){
    if (abs(tgt-pos) <3){
      pos = tgt;
    }
    else if (tgt>pos){
      pos = pos +3;
    }
    else if (tgt<pos){
      pos = pos -3;
    }
  }
  else{
    if (abs(tgt-pos) <1){
      pos = tgt;
    }
    else if (tgt>pos){
      pos = pos +1;
    }
    else if (tgt<pos){
      pos = pos -1;
    }
  }

}

void servoPercent(int servoNum, int percent){
  int pulselen = 0;
  int angle = 0;
  
  if (servoNum == ARM1PIN){
    angle = (100-percent)*rangeArm1[0] + (percent)*rangeArm1[1];
    //Serial.print("arm 1: ");
  }
  else if (servoNum == ARM2PIN){
    angle = (100-percent)*rangeArm2[0] + (percent)*rangeArm2[1];
    //Serial.print("arm 2: ");
  }
  else if (servoNum == ROTATIONPIN){
    angle = (100-percent)*rangeRotation[0] + (percent)*rangeRotation[1];
    //Serial.print("rotation: ");
  }

  angle = angle/100;
  //Serial.println(angle);
  //parameters for small servo
  if (servoNum == CLAWPIN){
    pulselen = map(angle, 0, 180, SMLSERVOMIN, SMLSERVOMAX);
  }
  else{ //params for big servo
    pulselen = map(angle, 0, 180, BIGSERVOMIN, BIGSERVOMAX);
  }
  
  pwm.setPWM(servoNum, 0, pulselen);
}

//claw functions
void openClaw(){
  for (int angle = 120; angle <= 180; angle++) {
    //servoAngle(CLAWPIN,angle);
    claw.write(angle);
    delay(20);
  }
}

void closeClaw(){
  for (int angle = 180; angle >= 120; angle--) {
    //servoAngle(CLAWPIN,angle);
    claw.write(angle);
    delay(20);
  }
}


// converts angle to PWM output for servo
void servoAngle(int servoNum, int angle){
  int pulselen = 0;

  //parameters for small servo
  if (servoNum == CLAWPIN || servoNum == ARM2PIN){
    pulselen = map(angle, 0, 180, SMLSERVOMIN, SMLSERVOMAX);
  }
  else{ //params for big servo
    pulselen = map(angle, 0, 180, BIGSERVOMIN, BIGSERVOMAX);
  }
  
  pwm.setPWM(servoNum, 0, pulselen);
  delay(10);
}
