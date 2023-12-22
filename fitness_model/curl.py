# Flask Model for the Curl Counter 

from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np

curl = Flask(__name__)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
video_capture = None

counter = 0
stage = None

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def process_image(frame):
    global counter, stage

    # Recolor image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Makking the detection 
    results = pose.process(image=image)

    # Recolor back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
        landmarks = results.pose_landmarks.landmark

        # Get coordinates
        shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        def Calculate_angle(a, b, c):
            a = np.array(a)  # first landmark - shoulder
            b = np.array(b)  # second landmark - elbow
            c = np.array(c)  # third landmark - wrist
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180 / np.pi)
            if angle > 180.0:
                angle = 360 - angle
            return angle

        # Calculate angle
        angle = Calculate_angle(shoulder, elbow, wrist)

        # Visualize angle
        cv2.putText(image, str(angle),
                    tuple(np.multiply(elbow, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        # Curl Logic :)
        if angle > 160:
            stage = "down"
        if angle < 30 and stage == 'down':
            stage = "up"
            counter += 1
            print(counter)
    except:
        pass

    # Render curl counter
    # Setup status box
    cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)

    # Rep data
    cv2.putText(image, 'REPS', (15, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, str(counter),
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

    # Stage data
    cv2.putText(image, 'STAGE', (65, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, stage,
                (60, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

    # Render detections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                               mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                               mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                               )

    return image

def generate_frames():
    global video_capture
    video_capture = cv2.VideoCapture(0)

    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        frame = process_image(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@curl.route('/')
def index():
    return render_template('curl.html')

@curl.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@curl.route('/stop_video_feed')
def stop_video_feed():
    global video_capture, counter, stage

    if video_capture is not None:
        video_capture.release()
        video_capture = None
    
    counter = 0
    stage = None

if __name__ == "__main__":
    curl.run(debug=True)
