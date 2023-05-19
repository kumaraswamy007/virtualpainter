import cv2 as cv
import numpy as np
import mediapipe
import os
import time
import HandTrackingModule as htm




#########################################

brushThickness = 15
eraserThickness = 100

#########################################

folder = "Header"
myList = os.listdir(folder)
print(myList)
overlayList = []

for imPath in myList:
    image = cv.imread(f"{folder}/{imPath}")
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
drawColor = (255,0,255)

cap = cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0,0

imgCanvas = np.zeros((720,1280,3),np.uint8)

while True:
    #1.Import Image
    success, img = cap.read()
    img = cv.flip(img,1)

    #2.Find Hand LandMarks
    img = detector.findHands(img)
    lmList, bbox = detector.findposition(img,draw=False)

    if len(lmList)!= 0:

        #print(lmList)
        x1,y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #print(x1,y1)
        #3.Checking which fingers are up
        fingers = detector.fingersUp()
        #fprint(fingers)
        #4.If Selection mode - two fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("SELECTION MODE")
            #Checking for the click
            if y1 <125:
                if 250 < x1 <450:
                   header =  overlayList[0]
                   drawColor = (255,0,255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255,0,0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0,255,0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0,0,0)
            cv.rectangle(img, (x1, y1 - 30), (x2, y2 + 30), drawColor, cv.FILLED)

        #5. if Drawing Mode - index finger is up
        if fingers[1] and fingers[2]==False:
            cv.circle(img,(x1,y1),15,drawColor,cv.FILLED)
            print("DRAWING MODE")
            if xp==0 and yp==0:
                xp,yp = x1,y1

            if drawColor == (0,0,0):
                cv.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)

            xp,yp = x1,y1

    imgGray = cv.cvtColor(imgCanvas,cv.COLOR_BGR2GRAY)
    _,imgInv = cv.threshold(imgGray,50,255,cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv,cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img,imgInv)
    img = cv.bitwise_or(img,imgCanvas)




    #Setting the Header Image
    img[0:125,0:1280] = header
    #img = cv.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv.imshow("VIRTUAL PAINTER",img)
    #cv.imshow("Canvas",imgCanvas)

    if cv.waitKey(35) & 0xff == ord("f"):
        break


cap.release()
cv.destroyAllWindows()
