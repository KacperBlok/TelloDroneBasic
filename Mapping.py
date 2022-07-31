import numpy as np
import KeyPressModule as kp
from djitellopy import tello
from time import sleep
import numpy as npy
import cv2
import math

########### Parameters for mapping #######################
ForwardSpeed = 117/10 # Forward Speed in cm/s (15cm/s)
AngularSpeed = 360/10 # Angular Speed Degrees/s (50d/s)
interval = 0.25

DistanceInterval = ForwardSpeed*interval
AngularInterval = AngularSpeed*interval
#########################################################
x = 500
y = 500
Angle = 0
yaw = 0

kp.init()
drone = tello.Tello()
drone.connect()
print('battery is ' + str(drone.get_battery()) + ' %')

points = [(0,0), (0,0)]

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    AngularSpeed = 50
    Distance = 0
    global x, y, Angle, yaw

    if kp.getKey("LEFT"):
        lr = -speed
        Distance = DistanceInterval
        Angle = -180

    elif kp.getKey("RIGHT"):
        lr = speed
        Distance = -DistanceInterval
        Angle = 180

    if kp.getKey("UP"):
        fb = speed
        Distance = DistanceInterval
        Angle = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        Distance = -DistanceInterval
        Angle = -90

    if kp.getKey("q"):
        ud = speed

    elif kp.getKey("w"):
        ud = -speed

    if kp.getKey("a"):
        yv = -AngularSpeed
        yaw -= AngularInterval

    elif kp.getKey("s"):
        yv = AngularSpeed
        yaw += AngularInterval

    if kp.getKey("k"): drone.takeoff()
    if kp.getKey("l"): drone.land()

    sleep(interval)
    Angle += yaw
    x += int(Distance * math.cos(math.radians(Angle)))
    y += int(Distance * math.sin(math.radians(Angle)))

    return [lr, fb, ud, yv, x, y]

def DrawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500)/100},{(points[-1][1] - 500)/100})meters',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)

while True:
    value = getKeyboardInput()
    drone.send_rc_control(value[0], value[1], value[2], value[3])
    sleep(0.05)

    img = np.zeros((1000, 1000, 3), npy.uint8)
    if (points[-1][0] != value[4] or points[-1][1] != value[5]):
        points.append((value[4], value[5]))
    DrawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
