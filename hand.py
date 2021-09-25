import cv2
from cvzone.HandTrackingModule import HandDetector

#get video cam
cap = cv2.VideoCapture(0)
cap.set(3,1280) # 3 is width, 1280 pixels
cap.set(4,720) # 4 is height, 720 pixels
colorR = (255,0,0)

detector = HandDetector(detectionCon=0.8) #confidence has to be .8 instead of default .5

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)


    if lmList:
        cursor = lmList[8] #x and y of tip of finger
        if(100<cursor[0]<300 and 100<cursor[1]<200):
            colorR = (0,255,0)
        else:
            colorR = (255,0,0)

    cv2.rectangle(img,(100,100),(200,200),colorR,cv2.FILLED)
    cv2.imshow("Image",img)
    cv2.waitKey(1)

