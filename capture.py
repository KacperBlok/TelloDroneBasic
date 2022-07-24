import cv2
from djitellopy import tello

drone = tello.Tello()
drone.connect()
print('battery is ' + str(drone.get_battery()) + ' %')

drone.streamon()

while True:
    img = drone.get_frame_read().frame  # capture image
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)  # display
    cv2.waitKey(1)
