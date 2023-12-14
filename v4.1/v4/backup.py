from flask import Flask, render_template, Response, session
import cv2
import numpy as np
from lib.YOLO_Video import video_detection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'prdct'

roi = (100, 100, 300, 300)  # Format: (x, y, width, height)
prev_gray = None

def calculate_average_speed(flow, roi):
    u, v = flow[roi[1]:roi[3], roi[0]:roi[2]].T
    magnitude = np.sqrt(u**2 + v**2)
    average_speed = np.mean(magnitude)
    return average_speed



def gen_frames1():
    cap1 = cv2.VideoCapture(0)
    while True:
        success, frame = cap1.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_frames2():
    global prev_gray 
    cap = cv2.VideoCapture("1.mp4")
    success, first_frame = cap.read()

    prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        step = 16
        h, w = gray.shape
        y, x = np.mgrid[step // 2:h:step, step // 2:w:step].reshape(2, -1).astype(int)
        fx, fy = flow[y, x].T

        lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
        lines = np.int32(lines + 0.5)

        flow_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.polylines(flow_img, lines, 0, (0, 255, 0), 1)

        average_speed = calculate_average_speed(flow, roi)
        cv2.putText(flow_img, f"Average Speed: {average_speed:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', flow_img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        prev_gray = gray

def generate_frames_web():
    capp = 0
    yolo_output = video_detection(capp)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        



@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    session.clear()
    return render_template('index.html')

@app.route("/webcam", methods=['GET','POST'])
def webcam():
    session.clear()
    return render_template('ui.html')


@app.route('/webapp')
def webapp():
    return Response(generate_frames_web(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route("/multicam", methods=['GET','POST'])
def multicam():
    session.clear()
    return render_template('video_pre.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
    return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
