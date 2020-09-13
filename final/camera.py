import cv2
import time
import numpy as np
from random import randint
from contourCoordinates import contourCoordinates

class Camera(object):
    def __init__(self):
        # Camera
        self.cap = cv2.VideoCapture(0)

        # Game
        self.pressed_a = False
        self.pressed_s = False
        self.pressed_d = False
        self.pressed_f = False
        self.score = 0
        self.bpm = 225
        self.positions = [250,450,650,850]
        self.colors = [(0,255,0),(0,0,255),(255,0,0),(125,125,125)]
        self.notes = self.notes_gen()

        # Processing
        # lower and upper bound for yellow color in HSV
        self.yellowLowerBound = np.array([22, 63, 100])
        self.yellowUpperBound = np.array([31, 255, 255])
        self.redLowerBound = np.array([36,25,25])
        self.redUpperBound = np.array([70,255,255])
        # initial frame variable
        self.first_frame = None
        # initial shape detection bool
        self.detected_shapes = False
        # list of shapes
        self.shapes = []
        # initial interaction point
        self.points = []
        #0 is left up, 1 is right up, 2 is left down, 3 is right down
        self.direction = -1
        
        # Set up opening and closing filter
        self.kernelOpen = np.ones((5, 5))
        self.kernelClose = np.ones((20, 20))

        self.fingerExists = False
        self.fingerInShape = False

        self.buffer = None

        self.topLeft1_X = 70
        self.topLeft1_Y = 70
        self.topLeft1_XW = 270
        self.topLeft1_XH = 270

        self.topRight1_X = 1000
        self.topRight1_Y = 70
        self.topRight1_XW = 1200
        self.topRight1_XH = 270
        
        self.botLeft1_X = 70
        self.botLeft1_Y = 450
        self.botLeft1_XW = 270
        self.botLeft1_XH = 650

        self.botRight1_X = 1000
        self.botRight1_Y = 450
        self.botRight1_XW = 1200
        self.botRight1_XH = 650

    def within_a(self, x, y):
        return (x >= 150) and (x <= 350) and (y >= 600) and (y <= 700)
    
    def within_s(self, x, y):
        return (x >= 350) and (x <= 550) and (y >= 600) and (y <= 700)
    
    def within_d(self, x, y):
        return (x >= 550) and (x <= 750) and (y >= 600) and (y <= 700)
    
    def within_f(self, x, y):
        return (x >= 750) and (x <= 950) and (y >= 600) and (y <= 700)

    def __del__(self):
        self.cap.release()

    def note_gen(self, y, idx):
        note = {"x":self.positions[idx], "y":-y, "color":self.colors[idx]}
        return note
    
    def notes_gen(self):
        notes = []
        offset = 82
        for i in range(180):
            idx = randint(0,3)
            notes.append(self.note_gen(i*offset, idx))
    
        return notes

    def draw_game(self, frame):
        frame = cv2.rectangle(frame, (150,600), (350,700), (0,255,0),3)
        frame = cv2.rectangle(frame, (350,600), (550,700), (0,0,255),3)
        frame = cv2.rectangle(frame, (550,600), (750,700), (255,0,0),3)
        frame = cv2.rectangle(frame, (750,600), (950,700), (125,125,125),3)
        for note in self.notes:
            x = note["x"]
            y = note["y"]
            frame = cv2.circle(frame, (x, y), 40, note["color"], -1)

            if self.pressed_a and self.within_a(x, y):
                frame = cv2.rectangle(frame, (150,600), (350,700), (0,255,0),-1)
                self.pressed_a = False
                self.score += 10
            elif self.pressed_s and self.within_s(x, y):
                frame = cv2.rectangle(frame, (350,600), (550,700), (0,0,255),-1)
                self.pressed_s = False
                self.score += 10
            elif self.pressed_d and self.within_d(x, y):
                frame = cv2.rectangle(frame, (550,600), (750,700), (255,0,0),-1)
                self.pressed_d = False
                self.score += 10
            elif self.pressed_f and self.within_f(x, y):
                frame = cv2.rectangle(frame, (750,600), (950,700), (125,125,125),-1)
                self.pressed_f = False
                self.score += 10

            note["y"] = note["y"] + int(self.bpm / 60)


    def get_frame_bytes(self):
        ret, img = self.cap.read()

        # capture first frame to recognize shapes
        if self.first_frame is None:
            self.first_frame = img
            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg.tobytes(), jpeg.tobytes()

        else:
            if not self.fingerExists:
                self.buffer = img

            # get original height and width of shape
            height, width, layers = img.shape
            # get smaller frame to capture shapes
            imgSmall = cv2.resize(self.buffer, (int(width/4), int(height/4)))
            # resize main frame so its easier to see
            img_copy = img
            img = cv2.resize(img, (int(width), int(height)))
            # get ratio to multiply shape contours by when drawing them
            ratio = img.shape[0] / float(imgSmall.shape[0])
        
            # transform smaller frame to find shape contours
            gray = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)[1]
        
            # get contours from transformed small frame
            cnts, h = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        
            # top-left
            cv2.circle(img,(int((self.topLeft1_X+self.topLeft1_XW)/2),int((self.topLeft1_Y+self.topLeft1_XH)/2)), 75, (0,255,255), 2)
            # top-right
            cv2.circle(img,(int((self.topRight1_X+self.topRight1_XW)/2),int((self.topRight1_Y+self.topRight1_XH)/2)), 75, (0,255,255), 2)
            # bot-left 
            cv2.circle(img,(int((self.botLeft1_X+self.botLeft1_XW)/2),int((self.botLeft1_Y+self.botLeft1_XH)/2)), 75, (0,255,255), 2)
            # bot-right
            cv2.circle(img,(int((self.botRight1_X+self.botRight1_XW)/2),int((self.botRight1_Y+self.botRight1_XH)/2)), 75, (0,255,255), 2)
        
            # masking image to get yellow color
            imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(imgHSV, self.yellowLowerBound, self.yellowUpperBound)
        
            # opens and closes logic
            maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernelOpen)
            maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
        
            # find contours of yellow color shapes
            maskFinal = maskClose
            conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
            if len(conts) > 0:
                self.fingerExists = True
            else:
                self.fingerExists = False
        
            found = False
            currently_in = {"shape": "", "x-co": 0, "area": 0}
            starting_y = 0
            ending_y = 0
            # draw yello color rectangle
            cv2.drawContours(img, conts, -1, (255, 0, 0), 3)
        
            for i in range(len(conts)):
                self.points.append({"innerList": []})
        
            
            
            # show original frame with shapes and yellow objects
            resized_img = cv2.resize(img, (int(width/2), int(height/2)))
            #cv2.imshow("image", resized_img)
            #cv2.imshow("thresh", thresh)


            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(resized_img,'Score: {}'.format(self.score),(10,500), font, 4,(255,255,255),1,cv2.LINE_AA)

            self.draw_game(img_copy)

            for i in range(len(conts)):
                x, y, w, h = cv2.boundingRect(conts[i])
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                self.topLeft2_X = x
                self.topLeft2_Y = y
                self.botRight2_X = x+w
                self.botRight2_Y = y+h
        
                if self.topLeft2_X > self.topLeft1_X and self.topLeft2_Y > self.topLeft1_Y and self.botRight2_X < self.topLeft1_XW and self.botRight2_Y < self.topLeft1_XH:
                    self.pressed_a = True
                    print("topleft")
                elif self.topLeft2_X > self.topRight1_X and self.topLeft2_Y > self.topRight1_Y and self.botRight2_X < self.topRight1_XW and self.botRight2_Y < self.topRight1_XH:
                    self.pressed_s = True
                    print("topright")
                elif self.topLeft2_X > self.botLeft1_X and self.topLeft2_Y > self.botLeft1_Y and self.botRight2_X < self.botLeft1_XW and self.botRight2_Y < self.botLeft1_XH: 
                    self.pressed_d = True
                    print("botleft")
                elif self.topLeft2_X > self.botRight1_X and self.topLeft2_Y > self.botRight1_Y and self.botRight2_X < self.botRight1_XW and self.botRight2_Y < self.botRight1_XH: 
                    self.pressed_f = True
                    print("botRight")

            ret, jpeg = cv2.imencode('.jpg', resized_img)
            ret, game_jpeg = cv2.imencode('.jpg', img_copy)
            return jpeg.tobytes(), game_jpeg.tobytes()

