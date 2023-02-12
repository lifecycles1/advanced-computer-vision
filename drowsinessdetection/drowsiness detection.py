import face_recognition
import cv2
import time
from scipy.spatial import distance as dist
import playsound
from threading import Thread
import numpy as np

MIN_EAR = 0.30
EYE_EAR_CONSEC_FRAMES = 10

COUNTER = 0
ALARM_ON = False

def sound_alarm(soundfile = "C:\\python\\advanced computer vision\\drowsinessdetection\\alarm.mp3"):
  playsound.playsound(soundfile)

def eye_aspect_ratio(eye):
  A = dist.euclidean(eye[1], eye[5])
  B = dist.euclidean(eye[2], eye[4])
  C = dist.euclidean(eye[0], eye[3])
  ear = (A + B) / (2 * C)
  return ear

def main():
  global COUNTER, ALARM_ON
  video_capture = cv2.VideoCapture(0)
  video_capture.set(3, 640)
  video_capture.set(4, 480)

  while True:
    ret, frame = video_capture.read()
    if ret == True:
      face_landmarks_list = face_recognition.face_landmarks(frame)
      for face_landmark in face_landmarks_list:
        leftEye = face_landmark['left_eye']
        rightEye = face_landmark['right_eye']

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # might need to add a little bit of weights to the ear because when eyes are naturally low for some reason the alarm goes off
        ear = (leftEAR + rightEAR) / 2

        lpts = np.array(leftEye)
        rpts = np.array(rightEye)

        cv2.polylines(frame, [lpts], True, (0, 0, 255), 2)
        cv2.polylines(frame, [rpts], True, (0, 0, 255), 2)

        if ear < MIN_EAR:
          COUNTER += 1
          if COUNTER >= EYE_EAR_CONSEC_FRAMES:
            if not ALARM_ON:
              ALARM_ON = True
              t = Thread(target=sound_alarm)
              t.daemon = True
              t.start()
          cv2.putText(frame, "Alert! you are feeling asleep", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        else:
          COUNTER = 0
          ALARM_ON = False
        cv2.putText(frame, "Ear: {:.2f}".format(ear), (250, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
          
      cv2.imshow("sleep detection", frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
      
  video_capture.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()