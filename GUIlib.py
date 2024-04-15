import cv2
import numpy as np

pressed_button = False


class GUI:
    def __init__(self):  # setup position
        self.h = 50
        self.w = 50
        self.x = 10
        self.y = 10
        self._track = False
        self._track_x = 0
        self._track_y = 0

    def __call__(self, img: np.ndarray, fingers_up: list[int], fingers_touch: list[int], landmark: list[list[int]],
                 buffer: list[str]):  # track finger
        if landmark[0] == (0, 0):
            return
        if fingers_touch[0] == 0:
            self._track = False
        elif self._track:
            self.x = landmark[8][0] - self._track_x
            self.y = landmark[8][1] - self._track_y
        elif self.x <= landmark[8][0] <= self.x + self.w and self.y <= landmark[8][1] <= self.y + self.h:
            self._track_x = landmark[8][0] - self.x
            self._track_y = landmark[8][1] - self.y
            self._track = True


class WindowGUI(GUI):
    def __init__(self):
        super().__init__()
        self.hide = True
        self.background_color = (255, 255, 255)
        self.name = 'window'
        self.title_color = (0, 0, 0)
        self.win_h = 100
        self.win_w = 210
        self.h = 30
        self.w = self.win_w - 50
        self.x = 200
        self.y = 400

    def __call__(self, img: np.ndarray, fingers_up: list[int], fingers_touch: list[int], landmark: list[list[int]],
                 buffer: list[str]):
        if self.hide:
            if buffer and buffer[-1] == f'open:{self.name}':
                buffer.pop()
                self.hide = False
        else:
            self.w = self.win_w - 50
            if (self.x + self.w <= landmark[8][0] <= self.x + self.win_w and self.y <= landmark[8][1] <= self.y + self.h
                    and fingers_touch[0]):
                self.hide = True
            super().__call__(img, fingers_up, fingers_touch, landmark, buffer)
            self.rectangle(img, 0, 0, self.w + 50, self.win_h + self.h, self.background_color)
            self.rectangle(img, 0, 0, self.w + 50, self.win_h, self.background_color)
            self.text(img, 10, self.win_h + self.h - 10, self.name, self.title_color)
            cv2.line(img, (self.x + self.w + 15, self.y + self.h // 2),
                     (self.x + self.w + 35, self.y + self.h // 2), (0, 0, 0), 2)

    def rectangle(self, img, x, y, w, h, color, radius=10, thickness=-1, line_type=cv2.LINE_AA):
        #  corners:
        #  p1 - p2
        #  |     |
        #  p4 - p3

        topLeft = (self.x + x, self.y - self.win_h + y)
        bottomRight = (self.x + x + w, self.y - self.win_h + y + h)
        p1 = topLeft
        p2 = (bottomRight[0], topLeft[1])
        p3 = bottomRight
        p4 = (topLeft[0], bottomRight[1])

        overlay = img.copy()
        if thickness < 0:  # // draw rectangle
            cv2.rectangle(overlay, (p1[0] + radius, p1[1]), (p3[0] - radius, p3[1]), color, thickness, line_type)
            cv2.rectangle(overlay, (p1[0], p1[1] + radius), (p3[0], p3[1] - radius), color, thickness, line_type)
        else:  # // draw straight lines
            cv2.line(overlay, (p1[0] + radius, p1[1]), (p2[0] - radius, p2[1]), color, thickness, line_type)
            cv2.line(overlay, (p2[0], p2[1] + radius), (p3[0], p3[1] - radius), color, thickness, line_type)
            cv2.line(overlay, (p4[0] + radius, p4[1]), (p3[0] - radius, p3[1]), color, thickness, line_type)
            cv2.line(overlay, (p1[0], p1[1] + radius), (p4[0], p4[1] - radius), color, thickness, line_type)

        if radius > 0:  # // draw arcs
            cv2.ellipse(overlay, (p1[0] + radius, p1[1] + radius), (radius, radius), 180.0, 0, 90, color, thickness,
                        line_type)
            cv2.ellipse(overlay, (p2[0] - radius, p2[1] + radius), (radius, radius), 270.0, 0, 90, color, thickness,
                        line_type)
            cv2.ellipse(overlay, (p3[0] - radius, p3[1] - radius), (radius, radius), 0.0, 0, 90, color, thickness,
                        line_type)
            cv2.ellipse(overlay, (p4[0] + radius, p4[1] - radius), (radius, radius), 90.0, 0, 90, color, thickness,
                        line_type)
        alpha = 0.6
        img[:] = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    def text(self, img, x, y, text, color, text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1):
        overlay = img.copy()
        cv2.putText(overlay, text, (self.x + x, self.y - self.win_h + y), text_fontFace, text_fontScale, color)
        alpha = 0.8
        img[:] = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    def button(self, img, x, y, w, h, text, color, action, fingers_touch, landmark,
               text_color=(0, 0, 0), text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1):
        global pressed_button
        self.rectangle(img, x, y, w, h, color)
        self.text(img, x + 10, y + h - 10, text, text_color,
                  text_fontFace=text_fontFace, text_fontScale=text_fontScale)
        if not fingers_touch[0]:
            pressed_button = False
        elif (not pressed_button and (self.x + x <= landmark[4][0] <= self.x + x + w)
                and (self.y - self.win_h + y <= landmark[4][1] <= self.y - self.win_h + y + h)):
            pressed_button = True
            action()

    def add_img(self, img, x, y, img2):
        h1, w1, c1 = img.shape
        h2, w2, c2 = img2.shape
        img[self.y - self.win_h + y:self.y - self.win_h + y + h2, self.x + x:self.x + x + w2] \
            = img2[max(0, -y):min(h2, h1 - y), max(0, -x):min(w2, w1 - x)]
