// Created 20170725 BY YunShuiXin
// Arduino  program to control Ultrasonic Ranging Module HC-SR04 and send position-distance information to Raspberry PI. 
// Raspberry PI react to control CMD and the position-distance information, the give conmand to the car.


#include <Wire.h>
#include <Servo.h>
#include <NewPing.h>
#include <stdio.h>
#include <ctype.h>

 
#define MAX_DISTANCE 100
#define SERVO_PIN_F 10 
#define ANGLE_INIT 80
#define ANGLE_BOUNDS 40
#define TRIGGER_PIN_F  11   
#define ECHO_PIN_F     12  
#define ANGLE_STEP 1

int Angle = ANGLE_INIT;
int dist_F = 0;
Servo Front_Servo;
NewPing Front_Sonar(TRIGGER_PIN_F, ECHO_PIN_F, MAX_DISTANCE);
int dir = 1;

char moveCMD = 'L';
bool is_lock_on=false;
const int servo_1_pin1 = 2;
const int servo_1_pin2 = 3;
const int servo_2_pin1 = 4;
const int servo_2_pin2 = 5;
const int servo_3_pin1 = 6;
const int servo_3_pin2 = 7;
const int servo_4_pin1 = 8;
const int servo_4_pin2 = 9;
bool is_servo_1_clockwise = 1;
bool is_servo_2_clockwise = 1;
bool is_servo_3_clockwise = 1;
bool is_servo_4_clockwise = 1;


void setup() 
{
	Wire.begin(8);                
	Wire.onReceive(receiveEvent);
	Wire.onRequest(requestEvent);       
	Front_Servo.attach(SERVO_PIN_F);

	pinMode(servo_1_pin1,OUTPUT);
	pinMode(servo_1_pin2,OUTPUT);
	pinMode(servo_2_pin1,OUTPUT);
	pinMode(servo_2_pin2,OUTPUT);
	pinMode(servo_3_pin1,OUTPUT);
	pinMode(servo_3_pin2,OUTPUT);
	pinMode(servo_4_pin1,OUTPUT);
	pinMode(servo_4_pin2,OUTPUT);
}

void loop() 
{  
	delay(20);
	Front_Servo.write(Angle);

	if (Angle >= ANGLE_INIT+ANGLE_BOUNDS || Angle <= ANGLE_INIT-ANGLE_BOUNDS) {dir = -dir;}
	Angle += (dir * ANGLE_STEP);
	dist_F=int(Front_Sonar.ping_cm());
	if (dist_F<=0){dist_F = 100;}
	
	/////////////////////////////////////////////////////
    if(moveCMD == 'W')
	{
		is_servo_1_clockwise = 1;
        is_servo_2_clockwise = 1;
        is_servo_3_clockwise = 1;
        is_servo_4_clockwise = 1;
	}
    else if(moveCMD == 'S')
	{
	    is_servo_1_clockwise = 0;
        is_servo_2_clockwise = 0;
        is_servo_3_clockwise = 0;
        is_servo_4_clockwise = 0;
	}
    else if(moveCMD == 'A')
	{
	    is_servo_1_clockwise = 1;
        is_servo_2_clockwise = 1;
        is_servo_3_clockwise = 0;
        is_servo_4_clockwise = 0;
	}
    else if(moveCMD == 'D')
	{
	    is_servo_1_clockwise = 0;
        is_servo_2_clockwise = 0;
        is_servo_3_clockwise = 1;
        is_servo_4_clockwise = 1;
	}
	
	else if(moveCMD == 'L')
	{
	    is_lock_on = true;
	}
	///////////////////////////////////////////////////////
	
	/////////////////////////////////////////////////////
	if (!is_lock_on)
	{
		if(is_servo_1_clockwise==1)
		{
			digitalWrite(servo_1_pin1,HIGH);
			digitalWrite(servo_1_pin2,LOW);
		}
		else
		{
			digitalWrite(servo_1_pin1,LOW);
			digitalWrite(servo_1_pin2,HIGH);
		}

		if(is_servo_2_clockwise==1)
		{
			digitalWrite(servo_2_pin1,HIGH);
			digitalWrite(servo_2_pin2,LOW);
		}
		else
		{
			digitalWrite(servo_2_pin1,LOW);
			digitalWrite(servo_2_pin2,HIGH);
		}

		if(is_servo_3_clockwise==1)
		{
			digitalWrite(servo_3_pin1,HIGH);
			digitalWrite(servo_3_pin2,LOW);
		}
		else
		{
			digitalWrite(servo_3_pin1,LOW);
			digitalWrite(servo_3_pin2,HIGH);
		}
		  
		if(is_servo_4_clockwise==1)
		{
			digitalWrite(servo_4_pin1,HIGH);
			digitalWrite(servo_4_pin2,LOW);
		}
		else
		{
			digitalWrite(servo_4_pin1,LOW);
			digitalWrite(servo_4_pin2,HIGH);
		}
	}

	else
	{
		digitalWrite(servo_1_pin1,LOW);
		digitalWrite(servo_1_pin2,LOW);
		digitalWrite(servo_2_pin1,LOW);
		digitalWrite(servo_2_pin2,LOW);
		digitalWrite(servo_3_pin1,LOW);
		digitalWrite(servo_3_pin2,LOW);
		digitalWrite(servo_4_pin1,LOW);
		digitalWrite(servo_4_pin2,LOW);
	}
	/////////////////////////////////////////////////////
}

void receiveEvent(int howMany) 
{

    while (Wire.available()) 
	{ 
		moveCMD= Wire.read(); 
	}
}

void requestEvent() 
{

    byte i2c_info[32];
    //i2c_info[0]=Angle;//to Processing
    i2c_info[0]=Angle;//to Python
    i2c_info[1]=dist_F;
    //i2c_info[2]=dist_B;
    Wire.write((byte *)&i2c_info,2);
    
}
