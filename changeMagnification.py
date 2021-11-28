#! /usr/bin/env python
# Date: 2019-01-18
# Author: Goran Lovric (with additions from C. M. Schlepuetz)
# License: GPL 3 (see LICENSE file in root folder)

import time
import sys
from epicsPV import epicsPV
from epicsMotor import epicsMotor


def setNewFocus(foc):
   print("Moving focus to: "+str(foc))
   chFocus.move(foc)
   chFocus.wait(poll=1)
   time.sleep(20)

def setNewXValue(xvalue):
   print("Moving X Basestage to: "+str(xvalue))
   chXBaseStage.move(xvalue)
   chXBaseStage.wait(poll=1)

def setNewZValue(zvalue):
   print("Moving Z Basestage to: "+str(zvalue))
   chZBaseStage.move(zvalue)
   chZBaseStage.wait(poll=1)

def setFESlitsValues(H_val,V_val):
   print("Setting Frontend slits values to (H,V): ("+str(H_val)+",",str(V_val)+")")
   chFESlits_H.putw(H_val)
   chFESlits_V.putw(V_val)

def getMagnification():
    return chMagnification.getw()

if __name__ == "__main__":
   if not len(sys.argv) == 2:
      print(">>>>Error!! Call the script as follows: 'python changeMagnification.py [4x/10x/20x]' ")
      exit(1)   

   desired_objective = sys.argv[1]

   if desired_objective not in ('4x', '10x', '20x'):
      print(">>>>Error!! Not supported objective: Chooser either 4x, 10x, or 20x")
      exit(1)

   if desired_objective == '4x':
      desired_magnification = 4.0
   if desired_objective == '10x':
      desired_magnification = 10.0  
   if desired_objective == '20x':
      desired_magnification = 20.0   

   '''
   -------------------------------------------------------
   (0) Define variables and Check state
   -------------------------------------------------------
   '''
   chFocus=epicsMotor('X02DA-ES1-MS1:FOC')
   chToggleLens=epicsPV("X02DA-ES1-MS1:LNS+")
   chMagnification=epicsPV("X02DA-ES1-MS:MAGNF")
   #chLensSelector=epicsPV("X02DA-ES1-MS1:LNSSEL")
   chXBaseStage=epicsMotor("X02DA-ES1-SMP1:TRX")
   chZBaseStage=epicsMotor("X02DA-ES1-SMP1:TRZ")
   chTomoPanelSampleInPos=epicsPV("X02DA-SCAN-SCN1:SMPIN")
   chFESlits_H=epicsPV("X02DA-FE-SHsize")
   chFESlits_V=epicsPV("X02DA-FE-SVsize")

   foc_4x = 2261
   foc_10x = 500
   foc_20x = 3155
   X_4x = 0
   X_10x = 0
   X_20x = 187
   FE4x_H = 1.484
   FE4x_V = 1.067
   FE10x_H = 0.8
   FE10x_V = 0.5
   FE20x_H = 0.65
   FE20x_V = 0.46
   Z_4x = -0
   Z_10x = 0
   Z_20x = 0

   magnificationState = str(getMagnification())
   print(magnificationState)

   if magnificationState == '4.0' and desired_objective == '4x':
      print("Already at desired magnification - Nothing to do!!!")
      exit(0)
   if magnificationState == '10.0' and desired_objective == '10x':
      print("Already at desired magnification - Nothing to do!!!")
      exit(0)
   if magnificationState == '20.0' and desired_objective == '20x':
      print("Already at desired magnification - Nothing to do!!!")
      exit(0)

   '''
   -------------------------------------------------------
   (1) Move focus to zero
   -------------------------------------------------------
   '''
   setNewFocus(0)

   '''
   -------------------------------------------------------
   (2) Change objective
   -------------------------------------------------------
   '''
   print("Changing objective ...")

   retries = 0
   while desired_magnification != getMagnification():
      chToggleLens.putWait(1)
      time.sleep(7)
      retries += 1
      if retries > 4:
         print(">>>>Error in objective change! State not supported...")
         exit(1)

   '''
   -------------------------------------------------------
   (3) Set focus in new objective
   -------------------------------------------------------
   '''
   print("Move focus to the correct value ...")
   while True:
      magnificationState = str(chMagnification.getw())
      if magnificationState == '4.0' and desired_objective == '4x':
         setNewFocus(foc_4x)
         break
      if magnificationState == '10.0' and desired_objective == '10x':
         setNewFocus(foc_10x)
         break
      if magnificationState == '20.0' and desired_objective == '20x':
         setNewFocus(foc_20x)
         break
      time.sleep(0.5)
   
   '''
   -------------------------------------------------------
   (4) Set new X-value
   -------------------------------------------------------
   '''
   magnificationState = str(chMagnification.getw())
   if magnificationState == '4.0':
      setNewXValue(X_4x)
      chTomoPanelSampleInPos.putw(X_4x)
   elif magnificationState == '10.0':
      setNewXValue(X_10x)
      chTomoPanelSampleInPos.putw(X_10x)
   elif magnificationState == '20.0':
      setNewXValue(X_20x)
      chTomoPanelSampleInPos.putw(X_20x)   

   '''
   -------------------------------------------------------
   (5) Set new Z-value
   -------------------------------------------------------
   '''
   if magnificationState == '4.0':
      setNewZValue(Z_4x)
   elif magnificationState == '10.0':
      setNewZValue(Z_10x)
   elif magnificationState == '20.0':
      setNewZValue(Z_20x) 
   '''
   -------------------------------------------------------
   (6) Set new FE-Slits values
   -------------------------------------------------------
   '''
   if magnificationState == '4.0':
      setFESlitsValues(FE4x_H,FE4x_V)
   elif magnificationState == '10.0':
      setFESlitsValues(FE10x_H,FE10x_V)
   elif magnificationState == '20.0':
      setFESlitsValues(FE20x_H,FE20x_V)  


   print("DONE: Changed magnification successfully!")
