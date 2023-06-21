import cv2
import mediapipe as mp
import time


class handdetector():
    def __int__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
            for halm in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, halm, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handno=0, draw=True):
        lmlist = []
        if self.result.multi_hand_landmarks:
            mHand = self.result.multi_hand_landmarks[handno]
            for id, lm in enumerate(mHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 20, (0, 255, 0), cv2.FILLED)

        return lmlist
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handdetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist)!=0:
            print(lmlist[4])
        cv2.resize(img, [500, 500])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
