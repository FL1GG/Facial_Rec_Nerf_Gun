import numpy as np
import cv2
import serial
from pyfirmata import Arduino, util
import time
import scipy as sc

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

board = Arduino('COM17')


# Pin 13  Direction B
# Pin 12  Direction A
# Pin 11  PWM B
# Pin 9   Brake A
# Pin 8   Brake B
# Pin 3   PWM A

# Left Side motors (120 = forward)
#motorX = board.get_pin('d:3:a') # back
#brakeX = board.get_pin('d:9:d')
#dirx = board.get_pin('d:13:d')

#brakeX.write(0)
#dirx.write(0)
#motorX.write(150)

pin11 = board.get_pin('d:11:p') #MotorXaxis
pin13 = board.get_pin('d:3:p') #MotorYaxis
pin5 = board.get_pin('d:5:s') #Trigger
board.digital[8].write(0)
board.digital[9].write(0)


pin11.write(.25)
"""
pin5.write(90)

time.sleep(1)

pin5.write(50)

time.sleep(.2)

pin5.write(90)

"""
#Motor B
def turnRight(rateX):
    board.digital[9].write(0)
    board.digital[13].write(0)
    pin11.write(rateX)

#Motor B
def turnLeft(rateX):
    board.digital[8].write(0)
    board.digital[13].write(1)
    pin11.write(rateX)

def turnX(rate):
    if(rate == 0):
        stopMotorB()
    elif(rate < 0):
        turnRight(np.absolute(rate))
    elif(rate > 0):
        turnLeft(np.absolute(rate))

#Motor A
def turnUp(rateX):
    board.digital[9].write(0)
    board.digital[12].write(0)
    pin13.write(rateX)

#Motor A
def turnDown(rateX):
    board.digital[9].write(0)
    board.digital[12].write(1)
    pin13.write(rateX)

def turnY(rate):
    if(rate == 0):
        stopMotorA()
    elif(rate > 0):
        turnUp(np.absolute(rate))
    elif(rate < 0):
        turnDown(np.absolute(rate))


def stopBoth():
    pin11.write(0.0)
    pin13.write(0.0)
    board.digital[8].write(1)
    board.digital[9].write(1)


def stopMotorB():
    pin11.write(0.0)
    board.digital[8].write(1)

def stopMotorA():
    pin13.write(0.0)
    board.digital[9].write(1)


cap = cv2.VideoCapture(1)

currentRateY = 0
currentRateX = 0

"""
while True:
    if(currentRateY >= .9):
        currentRateY = .8
    if(currentRateX >= .9):
        currentRateY = .8

    if(currentRateY <= -.9):
        currentRateY = -.8
    if(currentRateX <= -.9):
        currentRateX = -.8


    ret, img = cap.read()

    cv2.imshow("as", img)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        quit()

    if(key != 255):
        print key

    if key == 119:
        print "W"
        currentRateY = currentRateY + .1
        turnY(currentRateY)
    elif key == 115:
        print "S"
        currentRateY = currentRateY - .1
        turnY(currentRateY)


    elif key == 97:
        print "A"
        currentRateX = currentRateX + .1
        turnX(currentRateX)
    elif key == 100:
        print "D"
        currentRateX = currentRateX - .1
        turnX(currentRateX)

"""