#!/usr/bin/env python3

import pigpio
import MStepper
import time

pi = pigpio.pi()

#create a 5 micro-step stepper
m1 = MStepper.MStepper(pi,5)

#define your own GPIO pin

m1.CoilA = 17
m1.CoilB = 22
m1.CoilC = 18
m1.CoilD = 25
m1.PwmAC = 23
m1.PwmBD = 24

#set GPIO and calculate GPIO Table
m1.setGPIO()

#Activate coil and set position
m1.setStepper(0)
time.sleep(1.0)


#ok move half turn
m1.move(500)

#ok move to a specific position
#this will move full turn backward
#and move faster
m1.delay=0.001
m1.moveTo(0)

#ok let's do 10 micro-step
m1.MicroStep=10
m1.setGPIO()

#and do half turn

m1.delay=0.01
m1.moveTo(2000)

#de-activate coil
m1.stop()
