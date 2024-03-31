import cv2
import numpy as np
import PIL

track = False


class GUI:
    def __init__(self):  # setup position
        self.h = 50
        self.w = 50
        self.x = 10
        self.y = 10
        self.track = False

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer):  # track finger
        global track
        if landmark[0] == (0, 0):
            return
        if self.track:
            self.x = landmark[8][0] - self.w // 2
            self.y = landmark[8][1] - self.h // 2
        if fingers_touch[0] == 1 and self.x <= landmark[8][0] <= self.x + self.w \
                and self.y <= landmark[8][1] <= self.y + self.h and not track:
            self.track = True
            track = True
            self.x = landmark[8][0] - self.w // 2
            self.y = landmark[8][1] - self.h // 2
        if fingers_touch[0] == 0 and self.track:
            self.track = False
            track = False


class WindowGUI(GUI):
    def __init__(self):
        super().__init__()
        self.hide = True
        self.pressed_button = False
        self.background_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
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
            self.rectangle(img, 0, -self.title_h, self.win_w, self.h, self.background_color)
            self.text(img, 10, - 10, self.name, self.title_color)
            self.rectangle(img, self.w + 15, -self.title_h // 2, 20, 2, (0, 0, 0))

        else:
            self.rectangle(img, 0, -self.title_h, self.win_w, self.win_h, self.background_color)
            self.rectangle(img, 0, 0, self.win_w, self.win_h, self.background_color)
            self.text(img, 10, -10, self.name, self.title_color)
            self.rectangle(img, self.w + 15, -self.title_h // 2, 20, 2, (0, 0, 0))

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
                and (self.y + self.title_h + y <= landmark[4][1] <= self.y + self.title_h + y + h)):
            if not self.pressed_button:
                self.pressed_button = True
                action()
        elif not fingers_touch[0]:
            self.pressed_button = False

    @staticmethod
    def add_img(img, x, y, img2):
        h, w, c = img2.shape
        img[y:y + h, x:x + w] = img2
