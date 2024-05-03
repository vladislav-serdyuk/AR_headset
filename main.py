"""
Copyright (C) 2024  Vladislav Serdyuk

Этот файл — часть AR_headset.
AR_headset — свободная программа: вы можете перераспространять ее и/или
изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
в каком она была опубликована Фондом свободного программного обеспечения;
либо версии 3 лицензии, либо любой более поздней версии.
AR_headset распространяется в надежде, что она будет полезной, но БЕЗО ВСЯКИХ ГАРАНТИЙ;
даже без неявной гарантии ТОВАРНОГО ВИДА или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ.
Подробнее см. в Стандартной общественной лицензии GNU.
Вы должны были получить копию Стандартной общественной лицензии GNU вместе с этой программой.
Если это не так, см. <https://www.gnu.org/licenses/>.
"""

import json
import importlib

import cv2
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from HandTrackingModule import HandDetector
from flask import Flask, render_template, Response

segmentor = SelfiSegmentation(model=1)  # remove background
hand_detector = HandDetector(staticMode=False,
                             maxHands=1,
                             modelComplexity=1,
                             detectionCon=0.7,
                             minTrackCon=0.5)
app = Flask(__name__)  # server
cap = cv2.VideoCapture(0)
app_buffer = []


def find_distance(p1: tuple, p2: tuple):
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))


def process_image(frame: np.ndarray):
    """
    Распознаёт руки и накладывает на изображение интерфейс
    :param frame: входное изображение
    """
    copy_frame = frame.copy()
    hands = hand_detector.findHands(frame)
    if hands:
        hand1 = hands[0]  # Get the first hand detected
        landmark = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        fingers_up = hand1["fingersUp"]

        fingers_touch = []
        for tip_id in [8, 12, 16, 20]:
            distance = find_distance(landmark[4][0:2], landmark[tip_id][0:2])
            if distance < 30:
                fingers_touch.append(1)
            else:
                fingers_touch.append(0)

        for gui in Apps:
            gui(frame, fingers_up, fingers_touch, landmark, app_buffer)

        if hand_on_gui:
            min_x = max(bbox[0] - 20, 0)
            max_x = bbox[0] + bbox[2] + 20
            min_y = max(bbox[1] - 20, 0)
            max_y = bbox[1] + bbox[3] + 20
            frame[min_y:max_y, min_x:max_x] = (
                segmentor.removeBG(copy_frame[min_y:max_y, min_x:max_x], frame[min_y:max_y, min_x:max_x], 0.3))

        if debug:
            cv2.putText(frame, str(fingers_up), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            cv2.putText(frame, f'   {str(fingers_touch)}', (10, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            for cx, cy, cz in landmark:
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
    else:
        for gui in Apps:
            gui(frame, [0] * 5, [0] * 4, [(0, 0)] * 20, app_buffer)


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/script.js')
def script() -> str:
    return render_template('script.js')


@app.route('/video_feed')
def video_feed() -> Response:
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


def get_frame():
    """
        Получает изображение с камеры, обрабатывает, отправляет клиенту
        :return: Generator[bytes, Any, None]
    """
    _, frame = cap.read()  # get frame from capture
    h, w, c = frame.shape
    black_streak = np.zeros((h, int(w * 0.6), c), dtype=np.uint8)
    while True:
        _, frame = cap.read()  # get frame from capture
        process_image(frame)
        frame = np.concatenate((frame, black_streak, frame), axis=1)
        if show_window:
            cv2.imshow('video', frame)
            cv2.waitKey(1)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')


# settings
debug = True
hand_on_gui = True
show_window = True

with open('pkglist.json') as file:
    Apps = [importlib.import_module('pkg.' + pkg['dir'] + '.run').App()
            for pkg in json.JSONDecoder().decode(file.read()).values()]

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
