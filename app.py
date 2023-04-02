from flask import Flask, render_template, request, Response
import cv2

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        success, image = camera.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(cv2.VideoCapture(0)), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/save_video', methods=['POST'])
def save_video():
    with open('video.mp4', 'wb') as f:
        # f.write(request.data)
        f.write(request.files['video'].stream.read())
    return 'Video saved successfully!'


if __name__ == '__main__':
    app.run(debug=True)
