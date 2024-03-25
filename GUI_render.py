import cv2
import numpy as np
import pkg.clock.run
import pkg.paint.run

inited_guis = []
message = ''
guis = [pkg.clock.run, pkg.paint.run]


def init_gui():
    for gui in guis:
        inited_guis.append(gui.App())


def draw_gui(img: np.ndarray, fingers_up: list[int], fingers_touch: list[int], landmark: list[list[int]]):
    for gui in inited_guis:
        gui(img, fingers_up, fingers_touch, landmark)
    if message:
        h, w, c = img.shape
        cv2.putText(img, message, (100, h // 2), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
