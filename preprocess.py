import cv2
import numpy as np
def nothing(x):
    pass

Window = 'Trackbar'
hl = 'Hue Low'
hh = 'Hue High'
sl = 'Saturation Low'
sh = 'Saturation High'
vl = 'Value Low'
vh = 'Value High'

min_area = 500

cv2.namedWindow(Window, flags = cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar(hl, Window, 0, 179, nothing)
cv2.createTrackbar(hh, Window, 0, 179, nothing)
cv2.createTrackbar(sl, Window, 0, 255, nothing)
cv2.createTrackbar(sh, Window, 0, 255, nothing)
cv2.createTrackbar(vl, Window, 0, 255, nothing)
cv2.createTrackbar(vh, Window, 0, 255, nothing)

cv2.setTrackbarPos(hl, Window, 0)
cv2.setTrackbarPos(hh, Window, 179)
cv2.setTrackbarPos(sl, Window, 0)
cv2.setTrackbarPos(sh, Window, 255)
cv2.setTrackbarPos(vl, Window, 0)
cv2.setTrackbarPos(vh, Window, 255)





cap = cv2.VideoCapture(2)

while(cap.isOpened):
    ret, frame = cap.read()
    # cv2.imshow('Original', frame)

    # frame = cv2.GaussianBlur(frame, (5,5), 0)
    frame = cv2.medianBlur(frame, 3)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hul = cv2.getTrackbarPos(hl, Window)
    huh = cv2.getTrackbarPos(hh, Window)
    sal = cv2.getTrackbarPos(sl, Window)
    sah = cv2.getTrackbarPos(sh, Window)
    val = cv2.getTrackbarPos(vl, Window)
    vah = cv2.getTrackbarPos(vh, Window)

    # HSVLOW = np.array([hul, sal, val])
    # HSVHIGH = np.array([huh, sah, vah])

    # Laptop webcam
    # HSVLOW = np.array([144, 135, 0])
    # HSVHIGH = np.array([179, 255, 255])

    # Logitech webcam
    # HSVLOW = np.array([0, 108, 0])
    # HSVHIGH = np.array([7, 255, 255])

    # PSI webcam
    # HSVLOW = np.array([0, 147, 39])
    # HSVHIGH = np.array([11, 255, 228])

    # HSVLOW = np.array([0, 155, 95])
    # HSVHIGH = np.array([9, 255, 255])

    HSVLOW1 = np.array([0, 100, 40])
    HSVHIGH1 = np.array([10, 255, 228])

    HSVLOW2 = np.array([160, 110, 40])
    HSVHIGH2 = np.array([179, 255, 228])



    mask = cv2.inRange(hsv, HSVLOW1, HSVHIGH1)
    mask1 = mask.copy()
    mask2 = cv2.inRange(hsv, HSVLOW2, HSVHIGH2)
    mask1 = cv2.bitwise_or(mask1, mask2, mask = None)
    mask = mask1.copy()

    # mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
    # mask1 = mask.copy()

    # mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    # mask1 = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))

    mask1 = cv2.bitwise_not(mask1)

    maskedFrame = cv2.bitwise_and(frame, frame, mask = mask1)

    maskedFrame = cv2.morphologyEx(maskedFrame, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    maskedFrame = cv2.morphologyEx(maskedFrame, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))

    # maskedFrame = cv2.bitwise_and(frame, frame, mask = mask1)

    contours, hierarchy = cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) >= min_area:
            # x,y,w,h = cv2.boundingRect(cnt)
            # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.circle(frame,center,2,(0,0,255),3)

    cv2.imshow('Detected frame', frame)
    cv2.imshow('Masked frame', maskedFrame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()