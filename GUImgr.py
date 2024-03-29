import json
import importlib

import cv2
import numpy as np

inited_guis = []
message = ''
buffer = []

with open('pkglist.json') as file:
    guis = [importlib.import_module('pkg.' + pkg['dir'] + '.run')
            for pkg in json.JSONDecoder().decode(file.read()).values()]


def init_gui():
    for gui in guis:
        inited_guis.append(gui.App())


def draw_gui(img: np.ndarray, fingers_up: list[int], fingers_touch: list[int], landmark: list[list[int]]):
    global message
    err = 0
    for gui in inited_guis:
        # noinspection PyBroadException
        try:
            gui(img, fingers_up, fingers_touch, landmark, buffer)
        except Exception:
            err += 1
    if err:
        message = f'In {err} apps error'
    else:
        update_msg()
    if message:
        h, w, c = img.shape
        cv2.putText(img, message, (100, h // 2), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)


def update_msg():
    global message
    message = ''
