import cv2
import numpy as np

cam = cv2.VideoCapture(2)

min_area = 500

R = 0
C = (0, 0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break

    frame = cv2.GaussianBlur(frame, (5,5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSVLOW = np.array([144, 135, 0])
    # HSVHIGH = np.array([179, 255, 255])
    # HSVLOW = np.array([0, 180, 34])
    # HSVHIGH = np.array([10, 255, 255])

    HSVLOW = np.array([22, 60, 200])
    HSVHIGH = np.array([60, 255, 255])

    # mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
    # mask1 = mask.copy()


    HSVLOW1 = np.array([0, 110, 40])
    HSVHIGH1 = np.array([10, 255, 228])

    HSVLOW2 = np.array([160, 110, 40])
    HSVHIGH2 = np.array([179, 255, 228])



    mask = cv2.inRange(hsv, HSVLOW1, HSVHIGH1)
    mask1 = mask.copy()
    mask2 = cv2.inRange(hsv, HSVLOW2, HSVHIGH2)
    mask1 = cv2.bitwise_or(mask1, mask2, mask = None)
    mask = mask1.copy()


    maskedFrame = cv2.bitwise_and(frame, frame, mask = mask)

    maskedFrame = cv2.dilate(maskedFrame, np.ones((5,5), "uint8"), iterations = 1)
    maskedFrame = cv2.erode(maskedFrame, np.ones((5,5), "uint8"), iterations = 1)

    contours, hierarchy = cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    max_radius = 0.001
    largest_center = (0,0)

    for cnt in contours:
        if cv2.contourArea(cnt) >= min_area:
            # x,y,w,h = cv2.boundingRect(cnt)
            # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            R = radius
            C = center
            cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.circle(frame,center,2,(0,0,255),3)

            if(radius > max_radius):
                max_radius = radius
                largest_center = center

    cv2.imshow('Detected frame', frame)
    cv2.imshow('Masked frame', maskedFrame)
    cv2.imshow('Mask', mask)

    distance = (66 * 77)/(max_radius)
    # print distance
    print largest_center

    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        print R
        print C
        img_counter += 1

cam.release()

cv2.destroyAllWindows()