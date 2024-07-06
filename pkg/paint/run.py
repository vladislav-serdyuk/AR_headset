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
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.windows_height = 300
        self.window_width = 300
        self.name = 'Paint'
        self.art = np.zeros((self.window_width, self.windows_height))
        self.last_point = (-1, -1)

    def __call__(self, img):
        super().__call__(img)
        if not self.hide:
            if (self.fingers_touch[0] and self.x <= self.landmark[8][0] <= self.x + self.window_width
                    and self.y - self.windows_height <= self.landmark[8][1] <= self.y):
                if self.last_point != (-1, -1):
                    cv2.line(self.art, self.last_point, (self.landmark[8][0] - self.x, self.landmark[8][1] - self.y
                                                         + self.windows_height),
                             (1,), 2)
                self.last_point = (self.landmark[8][0] - self.x, self.landmark[8][1] - self.y + self.windows_height)
            else:
                self.last_point = (-1, -1)

            self.button(img, 0, 0, 30, 30, '', (0, 0, 255), self.clean)
            h, w, c = img.shape
            for i in range(self.window_width):
                for j in range(self.windows_height):
                    if self.art[i][j] == 1:
                        img[max(min(self.y - self.windows_height + i, h - 1), 0)][max(min(self.x + j, w - 1), 0)] = \
                            (0, 0, 0, 255)

    def clean(self):
        self.art = np.zeros((self.window_width, self.windows_height))
