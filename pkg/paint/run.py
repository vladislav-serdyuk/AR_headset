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

import cv2
import numpy as np

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self):
        super().__init__()
        self.win_h = 300
        self.win_w = 300
        self.name = 'Paint'
        self.art = np.zeros((self.win_w, self.win_h))
        self.last_point = (-1, -1)

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer):
        super().__call__(img, fingers_up, fingers_touch, landmark, buffer)
        if not self.hide:
            if (fingers_touch[0] and self.x <= landmark[8][0] <= self.x + self.win_w
                    and self.y - self.win_h <= landmark[8][1] <= self.y):
                if self.last_point != (-1, -1):
                    cv2.line(self.art, self.last_point, (landmark[8][0] - self.x, landmark[8][1] - self.y + self.win_h),
                             (1,), 2)
                self.last_point = (landmark[8][0] - self.x, landmark[8][1] - self.y + self.win_h)
            else:
                self.last_point = (-1, -1)

            self.button(img, 0, 0, 30, 30, '', (0, 0, 255), self.clean, fingers_touch, landmark)
            h, w, c = img.shape
            for i in range(self.win_w):
                for j in range(self.win_h):
                    if self.art[i][j] == 1:
                        img[max(min(self.y - self.win_h + i, h - 1), 0)][max(min(self.x + j, w - 1), 0)] = \
                            (0, 0, 0, 255)

    def clean(self):
        self.art = np.zeros((self.win_w, self.win_h))
