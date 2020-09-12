#!/usr/bin/env python
from flask import Flask, render_template, Response
import io
import cv2

app = Flask(__name__)
vc = cv2.VideoCapture(0)


@app.route('/')
def index():
    return render_template('index.html')


"""Video streaming generator"""
def gen():
    while True:
        read_return_code, frame = vc.read()
        encode_return_code, image_buffer = cv2.imencode('.jpg', frame)
        io_buf = io.BytesIO(image_buffer)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')
        """Will trigger the alogrithm in here"""
        """Then continously send String to the frontend"""


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)