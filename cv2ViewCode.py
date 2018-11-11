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

pin11 = board.get_pin('d:11:p') #MotorXaxis
pin13 = board.get_pin('d:3:p') #MotorYaxis
pin5 = board.get_pin('d:5:s')
board.digital[8].write(0)
board.digital[9].write(0)


#Motor B
def turnRight(rateX):
    board.digital[8].write(0)
    board.digital[13].write(0)
    pin11.write(rateX)

#Motor B
def turnLeft(rateX):
    board.digital[8].write(0)
    board.digital[13].write(1)
    pin11.write(rateX)

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


cap = cv2.VideoCapture(1)  # IMPORTANT
time.sleep(2)

widthMiddleCamera = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH) / 2)
heightMiddleCamera = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT) / 2)

print "(" + str(widthMiddleCamera) + ", " + str(heightMiddleCamera) + ")"

heightMiddleCamera = heightMiddleCamera


constX = .3
constY = .3

pin5.write(90)

while 1:
    ret, img = cap.read()

    if(ret==True):
        cv2.line(img, (widthMiddleCamera, 0), (widthMiddleCamera, heightMiddleCamera*2), (0, 0, 255), 2)
        cv2.line(img, (0, heightMiddleCamera), (widthMiddleCamera*2, heightMiddleCamera), (0, 0, 255), 2)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if(len(faces)<1):
            stopBoth()

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            imgRect = img[y:y + h, x:x + w]

            #internal box
            xwL = (x)
            xwG = (x+w)
            xwG = xwG - 5
            xwL = xwL + 5

            ywL =(y)
            ywG = (y+h)
            ywG = ywG - 5
            ywL = ywL + 5

            outString = ""

            if(widthMiddleCamera > xwG):
                outString = outString + "Turn Left "
                xmove = constX
                turnLeft((xmove))
            elif(widthMiddleCamera < xwL):
                outString = outString + "Turn Right "
                xmove = constX
                turnRight((xmove))
            else:
                outString = outString + "CenteredX "
                stopMotorB()

            if(heightMiddleCamera > ywG):
                outString = outString + "Turn Up"
                turnUp((constY))
            elif(heightMiddleCamera < ywL):
                outString = outString + "Turn Down"
                turnDown((constY))
            else:
                outString = outString + "CenteredY"
                stopMotorA()

            #print outString

            if (outString == "CenteredX CenteredY"):
                pin5.write(50)

                time.sleep(.2)

                pin5.write(90)

                time.sleep(.3)

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break




cap.release()
cv2.destroyAllWindows()
