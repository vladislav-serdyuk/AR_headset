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

from datetime import datetime
import math

import cv2
import numpy as np

from GUIlib import GUI


class App(GUI):
    def __init__(self):
        super().__init__()
        self.x = 10
        self.y = 10
        self.h = 50
        self.w = 50
        self.dig = False
        self.t_pre = 0

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer):
        super().__call__(img, fingers_up, fingers_touch, landmark, buffer)
        now = datetime.now()
        if fingers_touch[1] and (not self.t_pre) and self.x <= landmark[4][0] <= self.x + self.w \
                and self.y <= landmark[4][1] <= self.y + self.h:
            self.t_pre = 1
            self.dig = not self.dig
        elif (not fingers_touch[1]) and self.t_pre:
            self.t_pre = 0

        if self.dig:
            self.h = 45
            self.w = 215
            cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, now.strftime('%H:%M:%S'), (self.x, self.y + self.h - 5),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        else:
            self.h = 100
            self.w = 100
            cv2.circle(img, (self.x + self.w // 2, self.y + self.h // 2), self.h // 2, (255, 255, 255), cv2.FILLED)

            cv2.line(img, (self.x + self.w // 2, self.y + self.h // 2),
                     (self.x + int(self.w * (1 + math.sin((now.hour / 6 + now.minute / 360) * math.pi) * 0.7) / 2),
                      self.y + int(self.h * (1 - math.cos((now.hour / 6 + now.minute / 360) * math.pi) * 0.7) / 2)),
                     (0, 0, 0), thickness=3)

            cv2.line(img, (self.x + self.w // 2, self.y + self.h // 2),
                     (self.x + int(self.w * (1 + math.sin(now.minute * math.pi / 30) * 0.9) / 2),
                      self.y + int(self.h * (1 - math.cos(now.minute * math.pi / 30) * 0.9) / 2)), (0, 0, 0),
                     thickness=2)

            cv2.line(img, (self.x + self.w // 2, self.y + self.h // 2),
                     (self.x + int(self.w * (1 + math.sin(now.second * math.pi / 30) * 0.9) / 2),
                      self.y + int(self.h * (1 - math.cos(now.second * math.pi / 30) * 0.9) / 2)), (0, 0, 255),
                     thickness=2)
