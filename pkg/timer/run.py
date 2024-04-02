from datetime import datetime, timedelta
import os

import numpy as np
import cv2
import sounddevice as sd
import soundfile as sf

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self):
        super().__init__()
        self.y = 100
        self.win_h = 280
        self.win_w = 205
        self.name = 'Timer'
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.activ = False
        self.end_time = None
        self.file = os.path.dirname(__file__) + '/melodia.mp3'

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer: list):
        super().__call__(img, fingers_up, fingers_touch, landmark, buffer)
        if self.activ:
            now = datetime.now()
            _time: timedelta = self.end_time - now
            if _time > timedelta():
                self.hour, self.min, self.sec = (_time.days * 24 + _time.seconds // 3600, _time.seconds // 60 % 60,
                                                 _time.seconds % 60)
            else:
                self.reset()
                data, fs = sf.read(self.file)
                sd.play(data, fs)
        if self.hide:
            return

        self.rectangle(img, 0, 0, self.win_w, 40, (255, 255, 255))
        self.text(img, 30, 30, str(self.hour) + ':' + str(self.min) + ':' + str(self.sec), (0, 0, 0))

        self.button(img, 10, 50, 90, 40, '+1h', (0, 0, 230),
                    lambda: self.add_time('+1h'), fingers_touch, landmark)
        self.button(img, 105, 50, 90, 40, '-1h', (0, 0, 230),
                    lambda: self.add_time('-1h'), fingers_touch, landmark)
        self.button(img, 10, 95, 90, 40, '+10m', (0, 0, 230),
                    lambda: self.add_time('+10m'), fingers_touch, landmark)
        self.button(img, 105, 95, 90, 40, '-10m', (0, 0, 230),
                    lambda: self.add_time('-10m'), fingers_touch, landmark)
        self.button(img, 10, 140, 90, 40, '+1m', (0, 0, 230),
                    lambda: self.add_time('+1m'), fingers_touch, landmark)
        self.button(img, 105, 140, 90, 40, '-1m', (0, 0, 230),
                    lambda: self.add_time('-1m'), fingers_touch, landmark)

        if self.activ:
            self.button(img, 10, 185, 185, 40, 'Pause', (0, 0, 255),
                        self.pause, fingers_touch, landmark)
        else:
            self.button(img, 10, 185, 185, 40, 'Start', (0, 255, 0),
                        self.start, fingers_touch, landmark)

        self.button(img, 10, 230, 185, 40, 'Reset', (127, 127, 127),
                    self.reset, fingers_touch, landmark)

    def add_time(self, t):
        if self.activ:
            return
        if t == '+1h':
            self.hour += 1
        elif t == '-1h':
            self.hour -= 1
        elif t == '+10m':
            self.min += 10
        elif t == '-10m':
            self.min -= 10
        elif t == '+1m':
            self.min += 1
        elif t == '-1m':
            self.min -= 1

    def start(self):
        self.activ = True
        now = datetime.now()
        self.end_time = now + timedelta(hours=self.hour, minutes=self.min, seconds=self.sec)

    def pause(self):
        self.activ = False

    def reset(self):
        self.activ = False
        self.hour = 0
        self.min = 0
        self.sec = 0
