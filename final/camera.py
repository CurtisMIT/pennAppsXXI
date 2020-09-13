import cv2
import time
import numpy as np
from random import randint
from shapedetector import ShapeDetector
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

    def within_a(x, y):
        return (x >= 150) and (x <= 350) and (y >= 600) and (y <= 700)
    
    def within_s(x, y):
        return (x >= 350) and (x <= 550) and (y >= 600) and (y <= 700)
    
    def within_d(x, y):
        return (x >= 550) and (x <= 750) and (y >= 600) and (y <= 700)
    
    def within_f(x, y):
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

            if self.pressed_a and within_a(x, y):
                frame = cv2.rectangle(frame, (150,600), (350,700), (0,255,0),-1)
                self.pressed_a = False
                self.score += 10
            elif self.pressed_s and within_s(x, y):
                frame = cv2.rectangle(frame, (350,600), (550,700), (0,0,255),-1)
                self.pressed_s = False
                self.score += 10
            elif self.pressed_d and within_d(x, y):
                frame = cv2.rectangle(frame, (550,600), (750,700), (255,0,0),-1)
                self.pressed_d = False
                self.score += 10
            elif self.pressed_f and within_f(x, y):
                frame = cv2.rectangle(frame, (750,600), (950,700), (125,125,125),-1)
                self.pressed_f = False
                self.score += 10

            note["y"] = note["y"] + int(self.bpm / 60)


    def get_frame_bytes(self):
        ret, frame = self.cap.read()

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'Score: {}'.format(self.score),(10,500), font, 4,(255,255,255),1,cv2.LINE_AA)

        self.draw_game(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

