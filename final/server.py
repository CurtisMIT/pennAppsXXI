from flask import Flask, render_template, Response
from playsound import playsound
from camera import Camera
app = Flask(__name__)


@app.route('/')
def index():
    playsound('bp.mp3', False)
    return render_template('index.html')


"""Video streaming generator"""
def gen(camera):
    while True:
        frame_bytes = camera.get_frame_bytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes +
                b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(
        gen(Camera()),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
