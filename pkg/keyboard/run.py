import numpy as np
import cv2

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self):
        super().__init__()
        self.y = 20
        self.win_h = 220
        self.win_w = 490
        self.name = 'Keyboard'

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer: list):
        super().__call__(img, fingers_up, fingers_touch, landmark, buffer)
        if self.hide:
            return

        keys = [
            '1234567890=',
            'qwertyuiop\\',
            'asdfghjkl"\n',
            'zxcvbnm,.?/',
                ]

        for y, row in enumerate(keys):
            for x, c in enumerate(row):
                self.button(img, x*45, y*45, 40, 40, c, (200, 0, 0),
                            lambda k=c: buffer.append(k), fingers_touch, landmark)

        self.button(img, 0, 180, 490, 40, '', (200, 0, 0),
                    lambda: buffer.append(' '), fingers_touch, landmark)
