import cv2
import numpy as np


class GUI:
    def __init__(self):  # setup position
        self.h = 50
        self.w = 50
        self.x = 10
        self.y = 10
        self.track = False

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer):  # track finger
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
        self.pressed_button = False
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

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer):
        self.h = self.title_h
        self.w = self.win_w - 50
        super().__call__(img, fingers_up, fingers_touch, landmark, buffer)

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

    def rectangle(self, img, x, y, w, h, color, border_color=None):
        cv2.rectangle(img, (self.x + x, self.y + self.title_h + y), (self.x + x + w, self.y + self.title_h + y + h),
                      color, -1)
        if border_color is not None:
            cv2.rectangle(img, (self.x + x, self.y + self.title_h + y), (self.x + x + w, self.y + self.title_h + y + h),
                          border_color, 1)

    def text(self, img, x, y, text, color, text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1):
        cv2.putText(img, text, (self.x + x, self.y + self.title_h + y), text_fontFace, text_fontScale, color)

    def button(self, img, x, y, w, h, text, color, action, fingers_touch, landmark, border_color=None,
               text_color=(0, 0, 0), text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1):
        self.rectangle(img, x, y, w, h, color, border_color)
        self.text(img, x + 10, y + h - 10, text, text_color,
                  text_fontFace=text_fontFace, text_fontScale=text_fontScale)
        if (fingers_touch[0] and (self.x + x <= landmark[4][0] <= self.x + x + w)
                and (self.y + y <= landmark[4][1] <= self.y + self.title_h + y + h)):
            if not self.pressed_button:
                action()
                self.pressed_button = True
        else:
            self.pressed_button = False

    @staticmethod
    def add_img(img, x, y, img2):
        h, w, c = img2.shape
        img[x:x + w, y:y + h] = img2
