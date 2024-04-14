import json

import numpy as np
import cv2

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self):
        super().__init__()
        self.x = 100
        self.y = 100
        self.win_h = 0
        self.win_w = 0
        self.name = 'My App'
        self.apps = []
        with open('pkglist.json') as file:
            pkg_list: dict = json.JSONDecoder().decode(file.read())
        for app in pkg_list.values():
            name = app["info"]
            if name not in ['Menu', 'Clock']:
                self.apps.append(name)

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer: list):
        if fingers_up == [0, 1, 0, 0, 1]:
            self.hide = False
        if self.hide:
            return
        for i, app in enumerate(self.apps):
            x = i % 3 * 180
            y = i // 3 * 40
            self.button(img, x, y, 170, 30, app, (255, 255, 255), lambda a=app: self.open(buffer, a),
                        fingers_touch, landmark)

    def open(self, buffer: list, app):
        buffer.append(f'open:{app}')
        self.hide = True
