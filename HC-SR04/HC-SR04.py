#! /usr/bin/python
# -*- coding:utf-8 -*-
# checkdist1:
# trig to GPIO20/PIN38
# echo to GPIO21/PIN40
# checkdist2:
# trig to GPIO19/PIN37
# echo to GPIO26/PIN39

import RPi.GPIO as GPIO
import time

def checkdist1():

        #发出触发信号
        GPIO.output(20,GPIO.HIGH)
        #保持10us以上（我选择15us）
        time.sleep(0.000015)
        GPIO.output(20,GPIO.LOW)
        while not GPIO.input(21):
                pass
        #发现高电平时开时计时
        t1 = time.time()
        while GPIO.input(21):
                pass
        #高电平结束停止计时
        t2 = time.time()
        #返回距离，单位为米
        return (t2-t1)*340/2

def checkdist2():

        GPIO.output(19,GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(19,GPIO.LOW)
        while not GPIO.input(26):
                pass
        t1 = time.time()
        while GPIO.input(26):
                pass
        t2 = time.time()
        return (t2-t1)*340/2

GPIO.setmode(GPIO.BCM)
#第3号针，GPIO2
GPIO.setup(20,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(19,GPIO.OUT,initial=GPIO.LOW)
#第5号针，GPIO3
GPIO.setup(21,GPIO.IN)
GPIO.setup(26,GPIO.IN)

time.sleep(2)
try:
        while True:
                print ('Distance1: %0.2f m'%checkdist1(),'Distance2: %0.2f m'%checkdist2())
                time.sleep(0.1)
except KeyboardInterrupt:
        GPIO.cleanup()