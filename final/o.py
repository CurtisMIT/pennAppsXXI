import cv2
import time
from random import randint
from playsound import playsound


#notes = [{"x":250,"y":-40,"color":(0,255,0)},{"x":450,"y":-40,"color":(255,0,0)},{"x":650,"y":-40,"color":(0,0,255)}]
positions = [250,450,650,850]
colors = [(0,255,0),(0,0,255),(255,0,0),(125,125,125)]
pressed_a = False
pressed_s = False
pressed_d = False
pressed_f = False
score = 0

def note_gen(y, idx):
    return {"x": positions[idx], "y":-y, "color": colors[idx]}

def notes_gen():
    notes = []
    offset = 82
    for i in range(180):
        idx = randint(0,3)
        notes.append(note_gen(i*offset, idx))

    return notes

def within_a(x, y):
    return (x >= 150) and (x <= 350) and (y >= 600) and (y <= 700)

def within_s(x, y):
    return (x >= 350) and (x <= 550) and (y >= 600) and (y <= 700)

def within_d(x, y):
    return (x >= 550) and (x <= 750) and (y >= 600) and (y <= 700)

def within_f(x, y):
    return (x >= 750) and (x <= 950) and (y >= 600) and (y <= 700)

def draw_game(frame, bpm):
    frame = cv2.rectangle(frame, (150,600), (350,700), (0,255,0),3)
    frame = cv2.rectangle(frame, (350,600), (550,700), (0,0,255),3)
    frame = cv2.rectangle(frame, (550,600), (750,700), (255,0,0),3)
    frame = cv2.rectangle(frame, (750,600), (950,700), (125,125,125),3)
    for note in notes:
        x = note["x"]
        y = note["y"]
        frame = cv2.circle(frame, (x, y), 40, note["color"], -1)

        global pressed_a, pressed_s, pressed_d, pressed_f, score
        if pressed_a and within_a(x, y):
            frame = cv2.rectangle(frame, (150,600), (350,700), (0,255,0),-1)
            pressed_a = False
            score += 10
        elif pressed_s and within_s(x, y):
            frame = cv2.rectangle(frame, (350,600), (550,700), (0,0,255),-1)
            pressed_s = False
            score += 10
        elif pressed_d and within_d(x, y):
            frame = cv2.rectangle(frame, (550,600), (750,700), (255,0,0),-1)
            pressed_d = False
            score += 10
        elif pressed_f and within_f(x, y):
            frame = cv2.rectangle(frame, (750,600), (950,700), (125,125,125),-1)
            pressed_f = False
            score += 10

        note["y"] = note["y"] + int(bpm / 60)


def start():
    cap = cv2.VideoCapture(0)
    bpm = 225
    if cap.isOpened():
        pass
    else:
        cap.open()
    
    playsound('bp.mp3', False)
    while(True):
        global pressed_a, pressed_s, pressed_d, pressed_f, score
        ret, frame = cap.read()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'Score: {}'.format(score),(10,500), font, 4,(255,255,255),1,cv2.LINE_AA)
        draw_game(frame, bpm)
        cv2.imshow('og', frame)
        prev_time = time.time()

        key = cv2.waitKey(1) & 0xFF

        if key == ord('a'):
            pressed_a = True
            print('a')
        elif key == ord('s'):
            pressed_s = True
            print('s')
        elif key == ord('d'):
            pressed_d = True
            print('d')
        elif key == ord('f'):
            pressed_f = True
            print('f')
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

notes = notes_gen()
start()
