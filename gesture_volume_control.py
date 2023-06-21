import cv2
import time
import numpy as np
import math
import handtrackingmodule as htm
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam, hcam = 640,480
ptime = 0
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

detector = htm.handdetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,None)
volume = cast(interface,POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minvol = volRange[0]
maxvol = volRange[1]
vol = 0
volbar = 400
volper = 0
while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) !=0:
        #print(lmlist[4],lmlist[8])
        x, y = lmlist[4][1], lmlist[4][2]
        x1, y1 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x+x1)//2, (y+y1)//2
        cv2.circle(img,(x,y),15,(255,0,0),cv2.FILLED)
        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x,y), (x1,y1), (255,0,0),3)

        length = math.hypot(x1-x,y1-y)
        #print(length)
        #hand range 10 - 320
        # volume range -65 - 0
        vol = np.interp(length,[10,125],[minvol,maxvol])
        volbar = np.interp(length, [10, 125], [300,150])
        volper = np.interp(length, [10, 125], [0, 100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img,(50,150),(85,300),(0,255,0),3)
    cv2.rectangle(img, (50, int(volbar)), (85, 300), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volper)}%', (40, 420), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255, 0), 3)
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img,f'FPS:{int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
    cv2.resize(img,(500,500))
    cv2.imshow("image",img)
    cv2.waitKey(1)