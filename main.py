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
from threading import Thread
# from time import time

import cv2
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from HandTrackingModule import HandDetector
from flask import Flask, render_template, Response

print('Hi, this is AR_headset_soft by Vlad Serdyuk\r\n'
      'Project on github: https://github.com/vladislav-serdyuk/AR_headset')

with open('config.json') as config_file:
    config = json.JSONDecoder().decode(config_file.read())

segmentor = SelfiSegmentation(model=config['segmentor']['model'])  # remove background
hand_detector = HandDetector(static_mode=config['hand_detector']['static_mode'],
                             max_hands=config['hand_detector']['max_hands'],
                             model_complexity=config['hand_detector']['model_complexity'],
                             detection_con=config['hand_detector']['detection_con'],
                             min_track_con=config['hand_detector']['min_track_con'])
app = Flask(__name__)  # server

if config['camera']['index'] == -1:
    index = 0
    while True:  # auto search webcam
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            break
        cap.release()
        index += 1
else:
    cap = cv2.VideoCapture(config['camera']['index'])

app_buffer: list[str] = []  # see docs
message: list[str] = ['']  # see docs
cam_image: np.ndarray | None = None
gui_image: np.ndarray | None = None
result_image: np.ndarray | None = None
h, w, c = 0, 0, 0
fingers_touch = [0] * 4  # Указ с большим ... мизинец с большим
fingers_up = [0] * 5  # Большой ... мизинец
landmark = [(0, 0)] * 21  # see open-cv
Apps = []  # [index] = app object
windows_positions = {}  # {app.id: index}


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
        Получает изображение и отправляет клиенту
        :return: Generator[bytes, Any, None]
    """
    while True:
        if result_image is not None:
            # noinspection PyTypeChecker
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', result_image)[1].tobytes() + b'\r\n')


def find_distance(p1: tuple, p2: tuple):
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))


def load_apps():
    with open('pkglist.json') as file:
        Apps[:] = [
            importlib.import_module('pkg.' + pkg['dir'] + '.run').App(fingers_up, fingers_touch, app_buffer, message,
                                                                      landmark)
            for pkg in json.JSONDecoder().decode(file.read()).values()]
        windows_positions.clear()
        for i, _app in enumerate(Apps):
            windows_positions[_app.id] = i


def render_gui(frame: np.ndarray):
    global gui_image
    """
    Распознаёт руки и накладывает на изображение интерфейс
    :param frame: входное изображение
    """
    gui_img = np.zeros((h, w, c + 1), dtype=np.uint8)
    copy_frame = frame.copy()
    hands = hand_detector.find_hands(frame)
    if hands:
        hand1 = hands[0]  # Get the first hand detected
        landmark[:] = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        fingers_up[:] = hand1["fingersUp"]

        for _i, tip_id in enumerate([8, 12, 16, 20]):  # update fingers_touch
            distance = find_distance(landmark[4][0:2], landmark[tip_id][0:2])
            if distance < 30:
                fingers_touch[_i] = 1
            else:
                fingers_touch[_i] = 0

        for gui in Apps:
            try:
                gui(gui_img)
            except Exception as e:
                print('[WARNING] ERROR in app')
                print(type(e), e)

        if hand_on_gui:
            min_x = max(bbox[0] - 20, 0)
            max_x = bbox[0] + bbox[2] + 20
            min_y = max(bbox[1] - 20, 0)
            max_y = bbox[1] + bbox[3] + 20
            gui_img[min_y:max_y, min_x:max_x, :3] = segmentor.removeBG(copy_frame[min_y:max_y, min_x:max_x],
                                                                       cv2.cvtColor(gui_img[min_y:max_y, min_x:max_x],
                                                                                    cv2.COLOR_BGRA2BGR),
                                                                       0.3)

        if debug:
            cv2.putText(gui_img, str(fingers_up), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255, 255), 3)
            cv2.putText(gui_img, f'   {str(fingers_touch)}', (10, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255, 255),
                        3)
            for cx, cy, cz in landmark:
                cv2.circle(gui_img, (cx, cy), 5, (255, 0, 255, 255), cv2.FILLED)
    else:
        for gui in Apps:
            try:
                gui(gui_img)
            except Exception as e:
                print('[WARNING] ERROR in app')
                print(type(e), e)
    gui_image = gui_img
    process_message_for_system()


def process_message_for_system():
    cmd, *arg = message[0].split(':', maxsplit=1)
    if cmd == 'window-top':
        win = int(arg[0])
        pos = windows_positions[win]
        windows_positions[win], windows_positions[Apps[-1].id] = len(Apps) - 1, pos
        Apps[-1], Apps[pos] = Apps[pos], Apps[-1]
        message[0] = ''
    elif cmd == 'reload-apps':
        print('[LOG] reload apps')
        load_apps()
        message[0] = ''


def update_result_image_in_background():
    global result_image
    global gui_image
    global cam_image
    global h, w, c
    ret, frame = cap.read()  # get frame from capture
    if not ret:
        print("can't get frame from capture")
        return
    h, w, c = frame.shape
    black_streak = np.zeros((h, int(w * 0.6), c), dtype=np.uint8)
    # last_time = time()
    while True:
        ret, frame = cap.read()  # get frame from capture
        # frame = cv2.flip(frame, 1)
        if not ret:
            continue
        cam_image = frame
        if gui_image is not None:
            gui_image_temp = gui_image
            alpha = gui_image_temp[:, :, 3]
            gui_mask = cv2.merge([alpha, alpha, alpha]) / 255
            frame = (frame * (1 - gui_mask) + gui_image_temp[:, :, :3] * gui_mask).astype(dtype=np.uint8)
        frame = np.concatenate((frame, black_streak, frame), axis=1)
        result_image = frame
        if show_window:
            # if gui_image is not None:
            #     cv2.imshow('gui', gui_image)
            cv2.imshow('video', frame)
            cv2.waitKey(1)

        # print('fps: ', round(1 / (time() - last_time), 1))
        # last_time = time()


def update_gui_image_in_background():
    while True:
        if cam_image is not None:
            # noinspection PyTypeChecker
            render_gui(cam_image)


# settings
debug = config['other']['debug']
hand_on_gui = config['other']['hand_on_gui']
show_window = config['other']['show_window']

if __name__ == '__main__':
    print('[LOG] load apps')
    load_apps()
    print('[LOG] start "update gui image" daemon')
    update_gui_image_in_background_thread = Thread(target=update_gui_image_in_background, daemon=True)
    update_gui_image_in_background_thread.start()
    print('[LOG] start "update result image" daemon')
    update_result_image_in_background_thread = Thread(target=update_result_image_in_background, daemon=True)
    update_result_image_in_background_thread.start()
    print('[LOG] starting server')
    app.run(host='0.0.0.0')  # server run
    print('[LOG] server is stopped')
