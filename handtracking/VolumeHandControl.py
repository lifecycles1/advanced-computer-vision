import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

###############################
# wCam, hCam = 854, 520
# wCam, hCam = 960, 540
###############################

cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)
pTime = 0

detector = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
  success, img = cap.read()
  img = detector.findHands(img)
  lmList = detector.findPosition(img, draw=False)
  if len(lmList) != 0:
    # index finger
    x1, y1 = lmList[4][1], lmList[4][2]
    # thumb
    x2, y2 = lmList[8][1], lmList[8][2]
    # draw a circle on the index finger and thumb
    cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
    cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
    # draw a line between the index finger and thumb
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
    # find the center of the line between the index finger and thumb
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    # draw a circle in the center of the line (between the fingers)
    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

    # find the length of the line between the fingers (instead of using sqrt((x2 - x1)^2 + (y2 - y1)^2) 
    # we can just use math.hypot(x2 - x1, y2 - y1))
    length = math.hypot(x2 - x1, y2 - y1)
    
    # min max Hand range 20 - 200
    # min max Volume Range -96 - 0

    # tune the volume monotonically as the length of the line between the fingers changes
    vol = np.interp(length, [20, 200], [minVol, maxVol])
    volume.SetMasterVolumeLevel(vol, None)
    # reflect the volume change in the volBar and volPercentage
    volBar = np.interp(length, [20, 200], [400, 150])
    volPer = np.interp(length, [20, 200], [0, 100])

    # if length if line between fingers is less than 50
    if length < 50:
      # then change the color of the circle on the line in-between the fingers green
      cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)

  # draw a volBar frame
  cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
  # fill the volBar frame
  cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
  # volBar percentage text
  cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

  # create a frame rate counter
  cTime = time.time()
  fps = 1 / (cTime - pTime)
  pTime = cTime

  # display the frame rate counter
  cv2.putText(img, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

  # open up the camera image and when the user presses the 'q' key, exit the program
  cv2.imshow("Img", img)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break