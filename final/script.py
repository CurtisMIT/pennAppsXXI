from contourCoordinates import contourCoordinates
import cv2
import numpy as np

#from playsound import playsound
import time

# lower and upper bound for yellow color in HSV
yellowLowerBound = np.array([22, 63, 100])
yellowUpperBound = np.array([31, 255, 255])

redLowerBound = np.array([36,25,25])
redUpperBound = np.array([70,255,255])

# Get camera
cam = cv2.VideoCapture(0)
# initial frame variable
first_frame = None
# initial shape detection bool
detected_shapes = False
# list of shapes
shapes = []
# initial interaction point
points = []
# play bool
play_sound = False

direction = -1
#0 is left up, 1 is right up, 2 is left down, 3 is right down

# Set up opening and closing filter
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

fingerExists = False
fingerInShape = False

buffer = None

topLeft1_X = 70
topLeft1_Y = 70
topLeft1_XW = 270
topLeft1_XH = 270

topRight1_X = 1000
topRight1_Y = 70
topRight1_XW = 1200
topRight1_XH = 270

botLeft1_X = 70
botLeft1_Y = 450
botLeft1_XW = 270
botLeft1_XH = 650

botRight1_X = 1000
botRight1_Y = 450
botRight1_XW = 1200
botRight1_XH = 650


# Infinite for loop
while True:

    # read camera
    ret, img = cam.read()

    # capture first frame to recognize shapes
    if first_frame is None:
        first_frame = img
        continue

    if fingerExists == False:
        buffer = img

    # get original height and width of shape
    height, width, layers = img.shape
    # get smaller frame to capture shapes
    imgSmall = cv2.resize(buffer, (int(width/4), int(height/4)))
    # resize main frame so its easier to see
    img = cv2.resize(img, (int(width), int(height)))
    img_copy = img
    # get ratio to multiply shape contours by when drawing them
    ratio = img.shape[0] / float(imgSmall.shape[0])

    # transform smaller frame to find shape contours
    gray = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)[1]

    # get contours from transformed small frame
    cnts, h = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # top-left
    cv2.circle(img,(int((topLeft1_X+topLeft1_XW)/2),int((topLeft1_Y+topLeft1_XH)/2)), 75, (0,255,255), 2)
    # top-right
    cv2.circle(img,(int((topRight1_X+topRight1_XW)/2),int((topRight1_Y+topRight1_XH)/2)), 75, (0,255,255), 2)
    # bot-left 
    cv2.circle(img,(int((botLeft1_X+botLeft1_XW)/2),int((botLeft1_Y+botLeft1_XH)/2)), 75, (0,255,255), 2)
    # bot-right
    cv2.circle(img,(int((botRight1_X+botRight1_XW)/2),int((botRight1_Y+botRight1_XH)/2)), 75, (0,255,255), 2)

    # masking image to get yellow color
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, yellowLowerBound, yellowUpperBound)

    # opens and closes logic
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    # find contours of yellow color shapes
    maskFinal = maskClose
    conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(conts) > 0:
        fingerExists = True
    else:
        fingerExists = False

    found = False
    currently_in = {"shape": "", "x-co": 0, "area": 0}
    starting_y = 0
    ending_y = 0
    # draw yello color rectangle
    cv2.drawContours(img, conts, -1, (255, 0, 0), 3)

    for i in range(len(conts)):
        points.append({"innerList": []})

    
    for i in range(len(conts)):
        x, y, w, h = cv2.boundingRect(conts[i])
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        topLeft2_X = x
        topLeft2_Y = y
        botRight2_X = x+w
        botRight2_Y = y+h

        if topLeft2_X > topLeft1_X and topLeft2_Y > topLeft1_Y and botRight2_X < topLeft1_XW and botRight2_Y < topLeft1_XH:
            self.pressed_a = True
            print("topleft")
        elif topLeft2_X > topRight1_X and topLeft2_Y > topRight1_Y and botRight2_X < topRight1_XW and botRight2_Y < topRight1_XH:
            self.pressed_s = True
            print("topright")
        elif topLeft2_X > botLeft1_X and topLeft2_Y > botLeft1_Y and botRight2_X < botLeft1_XW and botRight2_Y < botLeft1_XH: 
            self.pressed_d = True
            print("botleft")
        elif topLeft2_X > botRight1_X and topLeft2_Y > botRight1_Y and botRight2_X < botRight1_XW and botRight2_Y < botRight1_XH: 
            self.pressed_f = True
            print("botRight")
    
    # show original frame with shapes and yellow objects
    resized_img = cv2.resize(img, (int(width/2), int(height/2)))
    cv2.imshow("image", resized_img)
    cv2.imshow("thresh", thresh)
    k =cv2.waitKey(1)
    

    if k & 0xFF== ord('q'): 
         break

cam.release()
cv2.destroyAllWindows()
