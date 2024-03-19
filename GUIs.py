import math
from datetime import datetime

import cv2
import numpy as np


class GUI:
    def __init__(self):  # setup position
        self.h = 50
        self.w = 50
        self.x = 10
        self.y = 10
        self.track = False

    def __call__(self, img, fingers_up, fingers_touch, landmark):  # track finger
        if self.track:
            self.x = landmark[8][0] - self.w // 2
            self.y = landmark[8][1] - self.h // 2
        if fingers_up[:] == [0, 1, 0, 0, 0] and self.x <= landmark[8][0] <= self.x + self.w \
                and self.y <= landmark[8][1] <= self.y + self.h:
            self.track = True
            self.x = landmark[8][0] - self.w // 2
            self.y = landmark[8][1] - self.h // 2
        if fingers_touch[0] and self.track:
            self.track = False


class WindowGUI(GUI):
    def __init__(self):
        super().__init__()
        self.hide = True
        self.background_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.border_thickness = 2
        self.name = 'window'
        self.title_h = 30
        self.title_color = (0, 0, 0)
        self.win_h = 100
        self.win_w = 210
        self.h = self.title_h
        self.w = self.win_w - 50
        self.x = 200
        self.y = 200
        self.t_pre = 0

    def __call__(self, img, fingers_up, fingers_touch, landmark):
        self.h = self.title_h
        self.w = self.win_w - 50
        super().__call__(img, fingers_up, fingers_touch, landmark)

        if ((not self.t_pre) and self.x + self.w <= landmark[8][0] <= self.x + self.win_w
                and self.y <= landmark[8][1] <= self.y + self.h):
            self.t_pre = 1
            self.hide = not self.hide
        elif ((not (self.x + self.w <= landmark[8][0] <= self.x + self.win_w
                    and self.y <= landmark[8][1] <= self.y + self.h)) and self.t_pre):
            self.t_pre = 0

        if self.hide:
            cv2.rectangle(img, (self.x, self.y), (self.x + self.win_w, self.y + self.h),
                          self.background_color, cv2.FILLED)
            cv2.rectangle(img, (self.x, self.y), (self.x + self.win_w, self.y + self.h),
                          self.border_color, self.border_thickness)
            cv2.putText(img, self.name, (self.x + 10, self.y + self.title_h - 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, self.title_color, 1)
            cv2.line(img, (self.x + self.w + 35, self.y + self.title_h // 2),
                     (self.x + self.w + 15, self.y + self.title_h // 2), self.border_color, thickness=2)
            cv2.line(img, (self.x + self.w, self.y),
                     (self.x + self.w, self.y + self.title_h), self.border_color, thickness=2)
        else:
            cv2.rectangle(img, (self.x, self.y), (self.x + self.win_w, self.y + self.win_h),
                          self.background_color, cv2.FILLED)
            cv2.rectangle(img, (self.x, self.y), (self.x + self.win_w, self.y + self.win_h),
                          self.border_color, self.border_thickness)
            cv2.line(img, (self.x, self.y + self.title_h), (self.x + self.win_w, self.y + self.title_h),
                     self.border_color, self.border_thickness)
            cv2.putText(img, self.name, (self.x + 10, self.y + self.title_h - 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, self.title_color, 1)
            cv2.line(img, (self.x + self.w + 35, self.y + self.title_h // 2),
                     (self.x + self.w + 15, self.y + self.title_h // 2), self.border_color, thickness=2)
            cv2.line(img, (self.x + self.w, self.y),
                     (self.x + self.w, self.y + self.title_h), self.border_color, thickness=2)


class Clock(GUI):
    def __init__(self):
        super().__init__()
        self.x = 10
        self.y = 10
        self.dig = False
        self.t_pre = 0

    def __call__(self, img, fingers_up, fingers_touch, landmark):
        super().__call__(img, fingers_up, fingers_touch, landmark)
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


class Paint(WindowGUI):
    def __init__(self):
        super().__init__()
        self.win_h = 400
        self.win_w = 400
        self.name = 'Paint'
        self.art = np.zeros((self.win_w, self.win_h))
        self.last_point = (-1, -1)

    def __call__(self, img, fingers_up, fingers_touch, landmark):
        super().__call__(img, fingers_up, fingers_touch, landmark)
        if not self.hide:
            if (self.x <= landmark[8][0] <= self.x + 30
                    and self.y + self.title_h <= landmark[8][1] <= self.y + self.title_h + 30):
                self.art = np.zeros((self.win_w, self.win_h))
                self.last_point = (-1, -1)
            elif (fingers_touch[0] and self.x <= landmark[8][0] <= self.x + self.win_w
                  and self.y + self.title_h <= landmark[8][1] <= self.y + self.win_h):
                if self.last_point != (-1, -1):
                    cv2.line(self.art, self.last_point, (landmark[8][0] - self.x, landmark[8][1] - self.y), (1,), 2)
                self.last_point = (landmark[8][0] - self.x, landmark[8][1] - self.y)
                # cv2.circle(self.art, (landmark[8][0] - self.x, landmark[8][1] - self.y), 5, (1,), -1)
            else:
                self.last_point = (-1, -1)

            cv2.rectangle(img, (self.x, self.y + self.title_h),
                          (self.x + 30, self.y + self.title_h + 30), (0, 0, 255), -1)
            h, w, c = img.shape
            for i in range(self.win_w):
                for j in range(self.win_h):
                    if self.art[i][j] == 1:
                        img[max(min(self.y + i, h - 1), 0)][max(min(self.x + j, w - 1), 0)] = (0, 0, 0)
