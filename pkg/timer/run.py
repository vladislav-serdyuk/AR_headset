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

from datetime import datetime, timedelta
import os

import sounddevice as sd
import soundfile as sf

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.windows_height = 280
        self.window_width = 205
        self.name = 'Таймер'
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.activ = False
        self.end_time = None
        self.file = os.path.dirname(__file__) + '/melodia.mp3'

    def __call__(self, img):
        super().__call__(img)
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

        self.rectangle(img, 0, 0, self.window_width, 40, (255, 255, 255))
        self.text(img, 30, 30, str(self.hour) + ':' + str(self.min) + ':' + str(self.sec), (0, 0, 0))

        self.button(img, 10, 50, 90, 40, '+1ч', (0, 0, 230), lambda: self.add_time('+1h'))
        self.button(img, 105, 50, 90, 40, '-1ч', (0, 0, 230), lambda: self.add_time('-1h'))
        self.button(img, 10, 95, 90, 40, '+10м', (0, 0, 230), lambda: self.add_time('+10m'))
        self.button(img, 105, 95, 90, 40, '-10м', (0, 0, 230), lambda: self.add_time('-10m'))
        self.button(img, 10, 140, 90, 40, '+1м', (0, 0, 230), lambda: self.add_time('+1m'))
        self.button(img, 105, 140, 90, 40, '-1м', (0, 0, 230), lambda: self.add_time('-1m'))

        if self.activ:
            self.button(img, 10, 185, 185, 40, 'Пауза', (0, 0, 255), self.pause)
        else:
            self.button(img, 10, 185, 185, 40, 'Старт', (0, 255, 0), self.start)

        self.button(img, 10, 230, 185, 40, 'Сброс', (127, 127, 127), self.reset)

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
