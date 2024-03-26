import typing

import cv2
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from cvzone.HandTrackingModule import HandDetector
from flask import Flask, render_template, Response

import GUImgr

segmentor = SelfiSegmentation()  # remove background
hand_detector = HandDetector()
app = Flask(__name__)  # server
cap = cv2.VideoCapture(0)


def process_image(frame: np.ndarray) -> np.ndarray:
    copy_frame = frame.copy()
    hands, frame = hand_detector.findHands(frame, draw=debug, flipType=True)
    if hands:
        hand1 = hands[0]  # Get the first hand detected
        landmark = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        fingers_up = hand_detector.fingersUp(hand1)

        fingers_touch = []

        for tip_id in [8, 12, 16, 20]:
            length, info, _ = hand_detector.findDistance(landmark[4][0:2], landmark[tip_id][0:2],
                                                         (frame if debug else None), color=(255, 0, 255), scale=10)
            if length < 40:
                fingers_touch.append(1)
            else:
                fingers_touch.append(0)

        GUI_render.draw_gui(frame, fingers_up, fingers_touch, landmark)

        if hand_on_gui:
            min_x = bbox[0] - 40
            max_x = bbox[0] + bbox[2] + 40
            min_y = bbox[1] - 40
            max_y = bbox[1] + bbox[3] + 40
            if min_x <= 0:
                min_x = 0
            if min_y <= 0:
                min_y = 0

            crop_img = copy_frame[min_y:max_y, min_x:max_x]
            src = segmentor.removeBG(crop_img, (0, 0, 0), 0.3)
            _, alpha = cv2.threshold(cv2.cvtColor(src, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)
            frame[min_y:max_y, min_x:max_x][alpha != 0] = src[alpha != 0]

        if debug:
            cv2.putText(frame, str(fingers_up), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            cv2.putText(frame, f'   {str(fingers_touch)}', (10, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            for mark_id, lm in enumerate(landmark):
                cx, cy, cz = lm
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
    else:
        GUI_render.draw_gui(frame, [0] * 5, [0] * 4, [(0, 0)] * 20)

    return frame


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/script.js')
def script():
    return render_template('script.js')


def get_frame():
    """
    Получает изображение с камеры, обрабатывает, отправляет клиенту
    :return: Generator[bytes, Any, None]
    """
    while True:
        ret, frame = cap.read()  # get frame from capture
        # frame = cv2.rotate(frame, 1)
        if flip_img:
            frame = cv2.flip(frame, 1)

        frame = process_image(frame)

        frame = np.concatenate((frame, frame), axis=1)
        if show_window:
            cv2.imshow('video', frame)

            if cv2.waitKey(1) == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                quit()

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


# setting
debug = True
hand_on_gui = True
flip_img = False
show_window = True
# end

GUImgr.init_gui()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
