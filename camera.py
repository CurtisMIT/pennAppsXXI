import cv2

class Camera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.y = 0

    def __del__(self):
        self.cap.release()

    def draw_game(self, frame, y):
        frame = cv2.circle(frame, (447,y), 63, (0,0,255), -1)
        frame = cv2.circle(frame, (247,y), 63, (0,255,0), -1)
        frame = cv2.circle(frame, (647,y), 63, (255,0,0), -1)

    def get_frame_bytes(self):
        ret, frame = self.cap.read()
        self.draw_game(frame, self.y)
        self.y = self.y + 10
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
