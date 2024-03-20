import typing

import cv2
import mediapipe as mp
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from flask import Flask, render_template, Response

import GUIs

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
segmentor = SelfiSegmentation()
app = Flask(__name__)
cap = cv2.VideoCapture(0)

inited_guis = []


def distance(p1, p2):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def init_gui():
    for gui in guis:
        inited_guis.append(gui())


def draw_gui(img, fingers_up, fingers_touch, landmark):
    for gui in inited_guis:
        gui(img, fingers_up, fingers_touch, landmark)
    if message:
        h, w, c = img.shape
        cv2.putText(img, message, (100, h // 2), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)


def process_image(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    with (mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands):
        process_frames = hands.process(rgb_frame)

        h, w, c = frame.shape
        tip_ids = [4, 8, 12, 16, 20]
        if process_frames.multi_hand_landmarks:
            hand = process_frames.multi_hand_landmarks[0]
            fingers_up = []
            fingers_touch = []

            if (distance(hand.landmark[tip_ids[0]], hand.landmark[17])
                    > distance(hand.landmark[tip_ids[0]],
                               typing.NamedTuple('xy', x=float, y=float)(hand.landmark[5].x * 2 - hand.landmark[17].x,
                                                                         hand.landmark[5].y * 2 - hand.landmark[17].y
                                                                         ))):
                fingers_up.append(1)
            else:
                fingers_up.append(0)

            for finger_id in range(1, 5):
                if distance(hand.landmark[tip_ids[finger_id]], hand.landmark[0]) \
                        < distance(hand.landmark[tip_ids[finger_id] - 2], hand.landmark[0]):
                    fingers_up.append(0)
                else:
                    fingers_up.append(1)

                if distance(hand.landmark[tip_ids[finger_id]], hand.landmark[4]) \
                        < distance(hand.landmark[3], hand.landmark[4]) * 1.2:
                    fingers_touch.append(1)
                else:
                    fingers_touch.append(0)

            landmark = []
            for mark_id, lm in enumerate(hand.landmark):
                landmark.append((int(lm.x * w), int(lm.y * h)))

            if hand_on_gui:
                crop_img = frame.copy()
                min_x = min(map(lambda x: x[0], landmark)) - 40
                max_x = max(map(lambda x: x[0], landmark)) + 40
                min_y = min(map(lambda x: x[1], landmark)) - 40
                max_y = max(map(lambda x: x[1], landmark)) + 40
                if min_x <= 0:
                    min_x = 0
                if min_y <= 0:
                    min_y = 0

                crop_img = crop_img[min_y:max_y, min_x:max_x]
                src = segmentor.removeBG(crop_img, (0, 0, 0), 0.3)
                _, alpha = cv2.threshold(cv2.cvtColor(src, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)

            draw_gui(frame, fingers_up, fingers_touch, landmark)

            if hand_on_gui:
                frame[min_y:max_y, min_x:max_x][alpha != 0] = src[alpha != 0]
            if debug:
                cv2.putText(frame, str(fingers_up), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                cv2.putText(frame, f'   {str(fingers_touch)}', (10, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                for hand in process_frames.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
                for mark_id, lm in enumerate(landmark):
                    cx, cy = lm
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        else:
            draw_gui(frame, [0] * 5, [0] * 4, [(0, 0)] * 20)

    return frame


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


def get_frame():
    while True:
        ret, frame = cap.read()
        if flip_img:
            frame = process_image(cv2.flip(frame, 1))
        else:
            frame = process_image(frame)

        # frame = np.concatenate((frame, frame), axis=1)
        if show_window:
            cv2.imshow('video', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()


# sitting
guis = [GUIs.Clock, GUIs.Paint]
message = ''
debug = True
hand_on_gui = True
flip_img = False
show_window = True
# end

init_gui()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
