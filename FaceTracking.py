import time
import cv2
import numpy as npy
from djitellopy import tello

drone = tello.Tello()
drone.connect()
print('battery is ' + str(drone.get_battery()) + ' %')

drone.streamon()
drone.takeoff()
drone.send_rc_xontrol(0, 0, 25, 0)
time.sleep(2.2)

width, height = 360, 240
fbRange = [6200, 6800]  # forward and backward range
pid = [0.4, 0.4, 0]
pError = 0


def FindFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceList = []
    myFaceListArea = []

    for (x, y, width, height) in faces:
        cv2.rectangle(img, (x, y), (x + width, y + height), (0, 0, 255), 2)
        cx = x + width // 2
        cy = y + height // 2
        area = width * height
        cv2.circle(img, (cx, cy, 5, (0, 255, 0), cv2.FILLED))
        myFaceList.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceList[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(drone, info, width, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - width // 2  # center of imgae
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(npy.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    print(speed, fb)

    if x == 0:
        speed = 0
        error = 0

    print(speed, fb)
    drone.send_rc_xontrol(0, fb, 0, speed)
    return error


while True:
    img = drone.get_frame_read().frame  # capture image
    img = cv2.resize(img, (w, h))
    img, info = FindFace(img)
    pError = trackFace(drone, info, width, pid, pError)
    print("Center", info[0], "Area", info[1])
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()
        break
