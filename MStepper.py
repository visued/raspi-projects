#!/usr/bin/env python3

import time
import pigpio
import numpy
import math

class MStepper:

  def __init__(self,pi,MicroStep):
    self.pi = pi
    self.CoilA = 17
    self.CoilB = 22
    self.CoilC = 18
    self.CoilD = 25
    self.PwmAC = 23
    self.PwmBD = 24
    self.MicroStep = int(MicroStep)
    self.delay = 0.01
    self.Position = 0
    self.gpioMask = 0
    self.PwmRange    = 1000
    self.Flag = False
    self.BuildMicroStepTable()

  def BuildMicroStepTable(self):
    self.TableSize = int(self.MicroStep * 4)
    self.coilTable = numpy.zeros(self.TableSize, dtype = numpy.uint32)
    self.pwmACTable = numpy.zeros(self.TableSize, dtype = numpy.int16)
    self.pwmBDTable = numpy.zeros(self.TableSize, dtype = numpy.int16)
    #calculate CoilTable for gpio
    HalfSize = int(self.TableSize/2)
    for i in range(HalfSize):
      self.coilTable[i] = 1 << self.CoilA
    for i in range(HalfSize,self.TableSize):
      self.coilTable[i] = 1 << self.CoilC
    for i in range(HalfSize):
      self.coilTable[i+self.MicroStep]= self.coilTable[i+self.MicroStep] | (1 << self.CoilB)
    for i in range(HalfSize, self.TableSize):
      self.coilTable[(i+self.MicroStep) % self.TableSize]= self.coilTable[(i+self.MicroStep) % self.TableSize] | (1 << self.CoilD)
    # calculate PWM
    for i in range(self.TableSize):
      PValue =  math.sqrt(math.fabs(math.sin(math.pi * i / (self.TableSize / 2.0))))
      self.pwmACTable[i]= math.floor(self.PwmRange * PValue)
      self.pwmBDTable[(i + self.MicroStep) % self.TableSize]= self.pwmACTable[i]

  def setGPIO(self):
    #set GPIO OUTPUT
    self.gpioMask = 1<<self.CoilA | 1<<self.CoilB | 1<<self.CoilC | 1<<self.CoilD
    self.pi.set_mode(self.CoilA,pigpio.OUTPUT)
    self.pi.set_mode(self.CoilB,pigpio.OUTPUT)
    self.pi.set_mode(self.CoilC,pigpio.OUTPUT)
    self.pi.set_mode(self.CoilD,pigpio.OUTPUT)
    self.pi.set_mode(self.PwmAC,pigpio.OUTPUT)
    self.pi.set_mode(self.PwmBD,pigpio.OUTPUT)
    #No power on coil
    self.pi.clear_bank_1(self.gpioMask)

    self.pi.set_PWM_frequency(self.PwmAC,1000000)
    self.pi.set_PWM_frequency(self.PwmBD,1000000)
    self.pi.set_PWM_range(self.PwmAC,self.PwmRange)
    self.pi.set_PWM_range(self.PwmBD,self.PwmRange)

    self.BuildMicroStepTable()
    self.Flag= True

  def setStepper(self,position):
     if(self.Flag):
       #set gpio
       index = position % self.TableSize
       setmask = self.coilTable[index]
       self.pi.clear_bank_1(self.gpioMask & ~setmask)
       self.pi.set_bank_1(setmask)
       #set PWM
       self.pi.set_PWM_dutycycle(self.PwmAC, self.pwmACTable[index])
       self.pi.set_PWM_dutycycle(self.PwmBD, self.pwmBDTable[index])
       self.Position= position

  def stop(self):
       self.pi.clear_bank_1(self.gpioMask)
       #set PWM
       self.pi.set_PWM_dutycycle(self.PwmAC,0)
       self.pi.set_PWM_dutycycle(self.PwmBD,0)


  def moveTo(self, Target):
    if Target == self.Position :
      return
    if self.Position < Target:
      direction=1
    else:
      direction=(-1)
    for i in range(self.Position,Target, direction) :
      self.setStepper(i)
      time.sleep(self.delay)

  def move(self, Target):
    Target = Target + self.Position
    self.moveTo(Target)
