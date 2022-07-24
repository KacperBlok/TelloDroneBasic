import KeyPressModule as kp
from djitellopy import tello
from time import sleep

kp.init()
drone = tello.Tello()
drone.connect()
print('battery is ' + str(drone.get_battery()) + ' %')

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    x = 75
    if kp.getKey("LEFT"): lr = -x
    elif kp.getKey("RIGHT"): lr = x

    if kp.getKey("UP"): fb = x
    elif kp.getKey("DOWN"): fb = -x

    if kp.getKey("q"): ud = x
    elif kp.getKey("w"): ud = -x

    if kp.getKey("a"): yv = x
    elif kp.getKey("s"): yv = -x

    if kp.getKey("k"): drone.takeoff()
    if kp.getKey("l"): drone.land()

    return [lr, fb, ud, yv]



while True:
    value = getKeyboardInput()
    drone.send_rc_control(value[0], value[1], value[2], value[3])
    sleep(0.05)
