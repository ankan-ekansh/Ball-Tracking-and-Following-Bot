import cv2
import numpy as np
import serial

try:
    ser = serial.Serial('/dev/rfcomm0', baudrate = 230400)
except:
    print('Check port')

# while(1):
#     c = (input())
#     ser.write(str(c))

cam = cv2.VideoCapture(2)

min_area = 500

# previous_radius = 0
# previous_center = (0, 0)
state = False
turn = ''
while(cam.isOpened):
    state = False
    ret, frame = cam.read()
    # cv2.imshow('Original', frame)

    # frame = cv2.GaussianBlur(frame, (5,5), 0)
    frame = cv2.medianBlur(frame, 3)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Laptop webcam
    # HSVLOW = np.array([144, 135, 0])
    # HSVHIGH = np.array([179, 255, 255])

    # Logitech webcam
    # HSVLOW = np.array([0, 108, 0])
    # HSVHIGH = np.array([7, 255, 255])

    # PSI webcam
    # HSVLOW = np.array([0, 147, 39])
    # HSVHIGH = np.array([11, 255, 228])


    # Arena Day

    # 1
    # HSVLOW = np.array([0, 143, 76])
    # HSVHIGH = np.array([10, 255, 255])

    # 2
    # HSVLOW = np.array([0, 164, 60])
    # HSVHIGH = np.array([10, 255, 255])

    # Arena Night

    # HSVLOW = np.array([0, 180, 34])
    # HSVHIGH = np.array([10, 255, 255])

    # Arena Night New Red Ball

    # HSVLOW = np.array([0, 155, 95])
    # HSVHIGH = np.array([9, 255, 255])




    # HSVLOW = np.array([])



    # HSVLOW1 = np.array([0, 100, 100])
    # HSVHIGH1 = np.array([10, 255, 255])

    # HSVLOW2 = np.array([160, 100, 100])
    # HSVHIGH2 = np.array([179, 255, 255])



    # HSVLOW1 = np.array([0, 147, 39])
    # HSVHIGH1 = np.array([10, 255, 228])

    # HSVLOW2 = np.array([160, 147, 39])
    # HSVHIGH2 = np.array([179, 255, 228])




    # mask = cv2.inRange(hsv, HSVLOW1, HSVHIGH1)
    # mask1 = mask.copy()
    # mask2 = cv2.inRange(hsv, HSVLOW2, HSVHIGH2)
    # mask1 = cv2.bitwise_or(mask1, mask2, mask = None)
    # mask = mask1.copy()

    # mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)

    HSVLOW1 = np.array([0, 110, 40])
    HSVHIGH1 = np.array([10, 255, 228])

    HSVLOW2 = np.array([160, 110, 40])
    HSVHIGH2 = np.array([179, 255, 228])



    mask = cv2.inRange(hsv, HSVLOW1, HSVHIGH1)
    mask1 = mask.copy()
    mask2 = cv2.inRange(hsv, HSVLOW2, HSVHIGH2)
    mask1 = cv2.bitwise_or(mask1, mask2, mask = None)
    mask = mask1.copy()

    mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))

    maskedFrame = cv2.bitwise_and(frame, frame, mask = mask1)

    # maskedFrame = cv2.dilate(maskedFrame, np.ones((5,5), "uint8"))
    # maskedFrame = cv2.erode(maskedFrame, np.ones((5,5), "uint8"))

    # contours, hierarchy = cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    max_radius = 0.001
    largest_center = (0, 0)

    for cnt in contours:
        if cv2.contourArea(cnt) >= min_area:
            # x,y,w,h = cv2.boundingRect(cnt)
            # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)

            if(radius > max_radius):
                state = True
                max_radius = radius
                largest_center = center
            
            cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.circle(frame,center,2,(0,0,255),3)

    # if(state == False):
    #     state = True
    
    # else:
    if(1):
        # distance = (28 * 141.5) / (max_radius)
        distance = (66 * 77)/(max_radius)
        print distance
        # if( (previous_center[0] < largest_center[0]) and (largest_center[0] - previous_center[0] > 4) ):
        #     print "right"
        #     ser.write(str(1))
        # elif( (previous_center[0] > largest_center[0]) and (previous_center[0] - largest_center[0] > 4) ):
        #     print "left"
        #     ser.write(str(1))
        # else:
        #     print "no turn"
        #     ser.write(str(0))

        if((state == False)):
            ser.flush()
            # ser.write(str(0))
            # delay(500)
            if(turn == 'left'):
                ser.write(str(9))
            else:
                ser.write(str(5))
            # not in frame
            # if(distance <= 30):
            # ser.write(str(0))
        else:
            if(largest_center[0] < 260):
                turn = 'left'
                if(distance >= 70):
                    ser.write(str(6))
                    print "nw"
                    # rotate left and forward
                else:
                    ser.write(str(3))
                    print "left turn"
                    # rotate left
            elif(largest_center[0] > 380):
                turn = 'right'
                if(distance >= 70):
                    ser.write(str(7))   
                    print "ne"
                    # rotate right and forward
                else:
                    ser.write(str(4))
                    print "right turn"
                    # rotate right
            else:
                if(distance >= 100):
                    ser.write(str(1))
                    print "forward"
                    # when camera aligned with centre of ball and distance is not minimum
                elif((distance > 70) and (distance < 100)):
                    ser.write(str(8))
                    print "slow forward"
                elif((distance > 50) and (distance < 70)):
                    ser.write(str(0))
                    print "stop"
                    # when camera aligned with centre of ball and distance is close to minimum
                else:
                    ser.write(str(2))
                    print "backward"
                    # when camera aligned with centre of ball and distance is less than minimum
    
    previous_center = largest_center
    previous_radius = max_radius
        





    cv2.imshow('Detected frame', frame)
    # cv2.imshow('Masked frame', maskedFrame)
    cv2.imshow('Mask', mask)



    if cv2.waitKey(1) & 0xFF == 27:
        ser.write(str(0))
        break

cam.release()
cv2.destroyAllWindows()
