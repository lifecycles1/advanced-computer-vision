import cv2
import time

## the minimizeWindow function is not working (can't install packages)
def minimizeWindow():
  print("Window minimized")
#   import win32gui, win32con
#   window = win32gui.GetForegroundWindow()
#   win32gui.ShowWindow(window, win32con.SW_MINIMIZE)

def cctv():
  video = cv2.VideoCapture(0)
  # frame width and height
  video.set(3, 640)
  video.set(4, 480)
  width = video.get(3)
  height = video.get(4)
  # welcoming messages
  print("Video resolution is set to ", width, " x ", height)
  print("Help-- \n1.Press esc key to exit.\n2.Press m key to minimize.")
  # video writer
  fourcc = cv2.VideoWriter_fourcc(*'XVID')
  # date and time
  date_time = time.strftime("recording %H-%M-%d -%m -%y")
  # avi or mp4 both are supported
  output = cv2.VideoWriter(date_time + '.avi', fourcc, 20.0, (int(width), int(height)))

  while True:
    check, frame = video.read()

    if check == True:
      frame = cv2.flip(frame, 1)
      t = time.ctime()
      cv2.rectangle(frame, (5, 5, 100, 20), (255, 255, 255), cv2.FILLED)
      cv2.putText(frame, "Camera 1", (20, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (5, 5, 5), 1)
      cv2.putText(frame, t, (int(width)-220, int(height)-20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (5, 5, 5), 1)
      cv2.imshow("CCTV Camera", frame)

      output.write(frame)
      # press esc key (27) to exit 
      if cv2.waitKey(1) == 27:
        print("Video footage saved in current directory")
        break
      # press m key to minimize
      elif cv2.waitKey(1) == ord('m'):
        minimizeWindow()
    else:
      print("Can't open camera, check configuration")
      break
  
  video.release()
  output.release()
  cv2.destroyAllWindows()

# main function
print("*"*80+"\n"+" "*30+"Welcome to cctv software\n"+"*"*80)
ask = int(input("Do you want to open the cctv?\n1. yes\n2. no\n>>> "))

if ask == 1:
  cctv()
elif ask == 2:
  print("Thank you for using our software")
  exit()