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

import numpy as np
import cv2

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self):
        super().__init__()
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
