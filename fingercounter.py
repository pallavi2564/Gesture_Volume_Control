import cv2
import time
import os

wcam, hcam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
folderpath = "images"
mylist = os.listdir(folderpath)
print(mylist)
overlaylist = []
for imgpath in mylist:
    image = cv2.imread(f'{folderpath}/{imgpath}') #to save images
    cv2.resize(image,(200, 200))
    overlaylist.append(image)  # to import images


while True:
    success, img = cap.read()
    img[0:133, 0:200] = overlaylist[0]
    cv2.imshow("image", img)
    cv2.waitKey(1)