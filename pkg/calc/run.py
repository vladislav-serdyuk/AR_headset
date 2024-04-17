"""
Copyright (C) 2024  Vladislav Serdyuk

Этот файл — часть AR_headset.
AR_headset — свободная программа: вы можете перераспространять ее и/или
изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
в каком она была опубликована Фондом свободного программного обеспечения;
либо версии 3 лицензии, либо любой более поздней версии.
Foobar распространяется в надежде, что она будет полезной, но БЕЗО ВСЯКИХ ГАРАНТИЙ;
даже без неявной гарантии ТОВАРНОГО ВИДА или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ.
Подробнее см. в Стандартной общественной лицензии GNU.
Вы должны были получить копию Стандартной общественной лицензии GNU вместе с этой программой.
Если это не так, см. <https://www.gnu.org/licenses/>.
"""

import numpy as np
import cv2

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self):
        super().__init__()
        self.win_h = 215
        self.win_w = 175
        self.name = 'Calculator'
        self.expression = ''

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer: list):
        super().__call__(img, fingers_up, fingers_touch, landmark, buffer)
        if self.hide:
            return

        self.rectangle(img, 0, 0, self.win_w, 40, (255, 255, 255))
        self.text(img, 10, 30, self.expression, (0, 0, 0))

        keys = [
            '123+',
            '456-',
            '789/',
            'c0=*',
                ]

        for y, row in enumerate(keys):
            for x, c in enumerate(row):
                self.button(img, x * 45, 40 + y * 45, 40, 40, c, (0, 0, 230),
                            lambda k=c: self.calc(k), fingers_touch, landmark)

    def calc(self, x):
        if x == 'c':
            self.expression = ''
        elif x == '=':
            try:
                self.expression = str(eval(self.expression))
            except SyntaxError:
                pass
            except ZeroDivisionError:
                pass
        else:
            self.expression += x
