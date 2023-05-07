import cv2
import mediapipe as mp

class HandDetector():
    def __init__(self,mode=False, maxHands=1, detectionCon=0.8, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(RGBimg)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList=[]

        if self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                    #print(id,lm)
                    h,w,c = img.shape
                    cx,cy = int(lm.x*w), int(lm.y*h) #prints pixel coordinates
                    #print (id, cx, cy)
                    lmList.append([id,cx,cy])

        return lmList

    def fingersUp(self,img):
        fingers=[0,0,0,0,0]
        handSide='r'
        lmList=self.findPosition(img)

        if len(lmList)!=0:
            
            #detecting left vs right hand
            if lmList[2][1]<lmList[17][1]:
                handSide='l'

            #checking 4 fingers
            for finger in range (1,6):

                if finger!=1:
                    #finger
                    if lmList[4*finger][2]<lmList[(4*finger)-1][2]: #if fingertip's y coord is less than last knuckle's y coord
                        fingers[finger-1]=1
                    else:
                        fingers[finger-1]=0    
                else: 
                    #thumb
                    #accounting for l or right hand since thumb detection relies on x value
                    if ((lmList[4][1]>lmList[3][1]) and handSide=='r')or \
                       ((lmList[4][1]<lmList[3][1]) and handSide=='l'):
                        fingers[0]=1
                    else:  
                        fingers[0]=0
 
        return fingers    


def main():
    cap = cv2.VideoCapture(0)   
    detector = HandDetector()    

    while True:
        success, img = cap.read() 
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        #if len(lmList) !=0:
            #print (lmList[4])
        print(detector.checkFingers(img))
        cv2.imshow("Image",img)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # if 'q' is pressed then quit
            break 

if __name__ == "__main__":
    main()   