import time
import os
import KeyPressModule as kp
from djitellopy import tello
import cv2
from time import sleep
import glob

kp.init()
drone = tello.Tello()
drone.connect()
print('battery is ' + str(drone.get_battery()) + ' %')
global img

drone.streamon()  # start stream


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    x = 75

    # Left arrow = go left and Right arrow= go right X
    if kp.getKey("LEFT"):
        lr = -x
    elif kp.getKey("RIGHT"):
        lr = x

    # UP arrow = go forward and DOWN arrow = go back
    if kp.getKey("UP"):
        fb = x
    elif kp.getKey("DOWN"):
        fb = -x

    # Q means go up and W means down
    if kp.getKey("q"):
        ud = x
    elif kp.getKey("w"):
        ud = -x

    # A and S = Rotation
    if kp.getKey("a"):
        yv = x
    elif kp.getKey("s"):
        yv = -x

    # K = take off
    # L = Land
    if kp.getKey("k"): drone.takeoff()
    if kp.getKey("l"): drone.land()

    listImage = []
    path = 'C:/Users/Kacper/PycharmProjects/Tello_Project1/Resources/photos/'

    if kp.getKey("z"):
        fileName = f'{time.time()}.jpg'
        filePath = f'Resources/photos/%s' %(fileName)

        cv2.imwrite(filePath, img)

        for file in glob.glob(path + '*.jpg'):
            print(file)
            base = os.path.basename(file)

            print(base)
            file = os.path.splitext(base)[0]
            print(file)
            listImage.append(file)

        if len(listImage) > 10:
            try:
                os.remove(path + min(listImage) + '.jpg')
            except:
                pass

        sleep(0.2)

    return [lr, fb, ud, yv]


while True:
    value = getKeyboardInput()
    drone.send_rc_control(value[0], value[1], value[2], value[3])
    img = drone.get_frame_read().frame  # capture image
    img = cv2.resize(img, (360, 240))  # setting size of window
    cv2.imshow("Image", img)  # display
    cv2.waitKey(1)

