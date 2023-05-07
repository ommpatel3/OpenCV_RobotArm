import serial
import HandTrackingModule as htm
import cv2
import mediapipe as mp
import math
import time

arduinoData = serial.Serial('com3',115200)

cap = cv2.VideoCapture(0)   
detector = htm.HandDetector()


def mapRange(x, in_min, in_max, out_min, out_max):
    num =  (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if (num < 0):
        num = 0
    elif (num > 100):
        num = 100
    return int(num)

def distBetween(a,b, lmList):
    return math.sqrt(pow(lmList[a][2]-lmList[b][2],2)+pow(lmList[a][1]-lmList[b][1],2))

def threeDigit(x):
    if (x < 10):
        return "00" + str(x)
    elif (x < 100):
        return "0" + str(x)
    else:
        return str(x)


while True:
    success, img = cap.read() 
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    cmd = ""

    if (len(lmList)!=0):
        
        #command is in the form of [arm1][rotation][arm2][claw]
        command = ""
        h,w,c = img.shape

        ##### GETTING ARM1 AND ROTATION -------------------------

        #use landmark 5 as the position indicator
        x = lmList[0][1]
        y = lmList[0][2]


        #converting to percent of screen travels
        x,y = int(x/w*100), int(y/h*100)

        #re mapping percent system to map 20 to 90% as full travel
        x,y = mapRange(x,20,80,0,100), 100- mapRange(y,35,95,0,100)

        #making them 3 digit
        x,y = threeDigit(x), threeDigit(y)

        ##### GETTING ARM2 --------------------------------------

        #compare distance between landmark 0 and 5 to get idea of wrist tilt
        tilt = threeDigit(mapRange(distBetween(0,5,lmList), 100,150,0,100))

        command = y + x + tilt

        ##### GETTING CLAW OPEN CLOSE ---------------------------

        #if dist between index and thumb less than 40 px,
        if (distBetween(4,8,lmList)<40):
            #red color line
            cv2.line(img,(lmList[4][1],lmList[4][2]),(lmList[8][1],lmList[8][2]),(20,138,7),4)
            #append "1" to the message
            command += "1"
            cv2.putText(img,"closed",(150,160),cv2.FONT_HERSHEY_PLAIN,3,(20,138,7),2)
        else:
            cv2.line(img,(lmList[4][1],lmList[4][2]),(lmList[8][1],lmList[8][2]),(66,125,245),4)
            command += "2"
            cv2.putText(img,"open",(150,160),cv2.FONT_HERSHEY_PLAIN,3,(66,125,245),2)

        
        cv2.putText(img,"arm 1:" + y,(10,40),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
        cv2.putText(img,"arm 2:" + tilt,(10,80),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
        cv2.putText(img,"rotation:" + x,(10,120),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
        cv2.putText(img,"claw:",(10,160),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
        
        cmd = command + '\r'
        arduinoData.write(cmd.encode())
        time.sleep(0.05)

    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # if 'q' is pressed then quit
        break 

