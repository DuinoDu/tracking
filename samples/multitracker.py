import numpy as np
import cv2

cv2.namedWindow("tracking")
#camera = cv2.VideoCapture("E:/code/opencv/samples/data/768x576.avi")
camera = cv2.VideoCapture("/home/duino/Videos/3/0.mp4")
tracker = cv2.MultiTracker("KCF")

w = 50
h = 50

bbox1 = (0,0, w, h)
bbox2 = (0,w*2, w, h)
bbox3 = (0,w*4, w, h)

bbox4 = (w,0, w, h)
bbox5 = (w,h*2, w, h)
bbox6 = (w,h*4, w, h)

bbox7 = (670, 200, w, h)


init_once = False

while camera.isOpened():
    ok, image=camera.read()
    image = cv2.resize(image, (image.shape[1]/2, image.shape[0]/2) )
    if not ok:
        print 'no image read'
        break

    if not init_once:
        # add a list of boxes:
        ok = tracker.add(image, (bbox1,bbox2,bbox3, bbox4, bbox5, bbox6, bbox7))
        # or add single box:
        #ok = tracker.add(image, bbox3)
        init_once = True

    ok, boxes = tracker.update(image)
    print ok, boxes
    print tracker.objects

    for newbox in boxes:
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(image, p1, p2, (200,0,0))

    cv2.imshow("tracking", image)
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break # esc pressed
