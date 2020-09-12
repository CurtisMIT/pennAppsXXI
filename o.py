import cv2
import time
from random import randint
from playsound import playsound


#notes = [{"x":250,"y":-40,"color":(0,255,0)},{"x":450,"y":-40,"color":(255,0,0)},{"x":650,"y":-40,"color":(0,0,255)}]
positions = [250,450,650,850]
colors = [(0,255,0),(0,0,255),(255,0,0),(125,125,125)]

def note_gen(y, idx):
    return {"x": positions[idx], "y":-y, "color": colors[idx]}

def notes_gen():
    notes = []
    offset = 82
    for i in range(180):
        idx = randint(0,3)
        notes.append(note_gen(i*offset, idx))

    return notes


def draw_game(frame, bpm, prev_time):
    frame = cv2.rectangle(frame, (150,600), (350,700), (0,255,0),3)
    frame = cv2.rectangle(frame, (350,600), (550,700), (0,0,255),3)
    frame = cv2.rectangle(frame, (550,600), (750,700), (255,0,0),3)
    frame = cv2.rectangle(frame, (750,600), (950,700), (125,125,125),3)
    for note in notes:
        frame = cv2.circle(frame, (note["x"], note["y"]), 40, note["color"], -1)
        note["y"] = note["y"] + int(bpm / 60)


def start():
    cap = cv2.VideoCapture(0)
    bpm = 225
    if cap.isOpened():
        pass
    else:
        cap.open()
    
    prev_time = time.time()
    playsound('bp.mp3', False)
    while(True):
        ret, frame = cap.read()
        draw_game(frame, bpm, prev_time)
        cv2.imshow('og', frame)
        prev_time = time.time()

        key = cv2.waitKey(1) & 0xFF

        if key == ord('a'):
            print('a')
        elif key == ord('s'):
            print('s')
        elif key == ord('d'):
            print('d')
        elif key == ord('f'):
            print('f')
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

notes = notes_gen()
start()
