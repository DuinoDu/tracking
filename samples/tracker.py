import numpy as np
import cv2

cv2.namedWindow("tracking")
videofile="/home/duino/tmp/python/opencv/test.avi"
camera = cv2.VideoCapture(videofile)
bbox = (220, 180, 80, 80)
tracker = cv2.Tracker_create("KCF")
init_once = False
cnt = 0

h, w = 480, 640
video = cv2.VideoWriter("kcf_1.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 10.0, (w, h), True)

while camera.isOpened():
    ok, image=camera.read()
    if not ok:
        print 'no image read'
        break

    if cnt == 30:
        tracker = cv2.Tracker_create("KCF")
        ok = tracker.init(image, bbox)

    if not init_once:
        ok = tracker.init(image, bbox)
        init_once = True

    ok, newbox = tracker.update(image)

    if ok:
        print ok, newbox
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(image, p1, p2, (255,0,255), 3)

    cv2.imshow("tracking", image)
    video.write(image)
    k = cv2.waitKey(500) & 0xff
    if k == 27 : 
        break
    cnt += 1
video.release()
