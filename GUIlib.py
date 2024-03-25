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

    def button(self, img, x, y, w, h, color, text, action, fingers_touch, landmark, text_color=(0, 0, 0),
               text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1):
        cv2.rectangle(img, (self.x + x, self.y + y), (self.x + x + w, self.y + y + h), color, -1)
        cv2.putText(img, text, (self.x + x + 10, self.y + y + h - 10), text_fontFace, text_fontScale, text_color)
        if (fingers_touch[0] and (self.x + x <= landmark[4][0] <= self.x + x + w)
                and (self.y + y <= landmark[4][1] <= self.y + y + h)):
            print('cls')
            print(fingers_touch[0])
            action()
