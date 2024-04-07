import cv2
import numpy as np
import PIL

track = False
index = 0


class GUI:
    def __init__(self):  # setup position
        global index
        self.h = 50
        self.w = 50
        self.x = 10
        self.y = 10
        self.track = False
        self.track_x = 0
        self.track_y = 0
        self.index = index
        index += 1

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer):  # track finger
        global track
        if landmark[0] == (0, 0):
            return
        if self.track:
            self.x = landmark[8][0] - self.track_x
            self.y = landmark[8][1] - self.track_y
        if fingers_touch[0] == 1 and self.x <= landmark[8][0] <= self.x + self.w \
                and self.y <= landmark[8][1] <= self.y + self.h and not track:
            self.track_x = landmark[8][0] - self.x
            self.track_y = landmark[8][1] - self.y
            self.track = True
            track = True
            self.x = landmark[8][0] - self.track_x
            self.y = landmark[8][1] - self.track_y
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
        self.hide_w = 130

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer):
        self.h = self.title_h
        if self.hide:
            self.w = self.hide_w
        else:
            self.w = self.win_w - 50
        super().__call__(img, fingers_up, fingers_touch, landmark, buffer)

        if ((not self.t_pre) and self.x + self.w <= landmark[8][0] <= self.x + self.w + 50
                and self.y <= landmark[8][1] <= self.y + self.h) and fingers_touch[0] and not track:
            self.t_pre = 1
            self.hide = not self.hide
        elif ((not (self.x + self.w <= landmark[8][0] <= self.x + self.w + 50
                    and self.y <= landmark[8][1] <= self.y + self.h)) or not fingers_touch[0]) and self.t_pre:
            self.t_pre = 0

        if self.hide:
            self.rectangle(img, 0, self.win_h, self.hide_w + 50, self.h, self.background_color)
            self.text(img, 10, self.win_h + self.title_h - 10, self.name, self.title_color)
            cv2.line(img, (self.x + self.w + 15, self.y + self.title_h // 2),
                     (self.x + self.w + 35, self.y + self.title_h // 2), (0, 0, 0), 2)

        else:
            self.rectangle(img, 0, 0, self.win_w, self.win_h + self.title_h, self.background_color)
            self.rectangle(img, 0, 0, self.win_w, self.win_h, self.background_color)
            self.text(img, 10, self.win_h + self.title_h - 10, self.name, self.title_color)
            cv2.line(img, (self.x + self.w + 15, self.y + self.title_h // 2),
                     (self.x + self.w + 35, self.y + self.title_h // 2), (0, 0, 0), 2)

    def rectangle(self, img, x, y, w, h, color, radius=10, thickness=-1, line_type=cv2.LINE_AA):
        overlay = img.copy()

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

        if thickness < 0:
            # // draw rectangle
            cv2.rectangle(overlay, (p1[0] + radius, p1[1]), (p3[0] - radius, p3[1]), color, thickness, line_type)
            cv2.rectangle(overlay, (p1[0], p1[1] + radius), (p3[0], p3[1] - radius), color, thickness, line_type)
        else:
            # // draw straight lines
            cv2.line(overlay, (p1[0] + radius, p1[1]), (p2[0] - radius, p2[1]), color, thickness, line_type)
            cv2.line(overlay, (p2[0], p2[1] + radius), (p3[0], p3[1] - radius), color, thickness, line_type)
            cv2.line(overlay, (p4[0] + radius, p4[1]), (p3[0] - radius, p3[1]), color, thickness, line_type)
            cv2.line(overlay, (p1[0], p1[1] + radius), (p4[0], p4[1] - radius), color, thickness, line_type)

        # // draw arcs
        if radius > 0:
            cv2.ellipse(overlay, (p1[0] + radius, p1[1] + radius), (radius, radius), 180.0, 0, 90, color, thickness,
                        line_type)
            cv2.ellipse(overlay, (p2[0] - radius, p2[1] + radius), (radius, radius), 270.0, 0, 90, color, thickness,
                        line_type)
            cv2.ellipse(overlay, (p3[0] - radius, p3[1] - radius), (radius, radius), 0.0, 0, 90, color, thickness,
                        line_type)
            cv2.ellipse(overlay, (p4[0] + radius, p4[1] - radius), (radius, radius), 90.0, 0, 90, color, thickness,
                        line_type)
        alpha = 0.6
        new_img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
        img[:][:] = new_img

    def text(self, img, x, y, text, color, text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1):
        overlay = img.copy()
        cv2.putText(overlay, text, (self.x + x, self.y - self.win_h + y), text_fontFace, text_fontScale, color)
        alpha = 0.8
        new_img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
        img[:][:] = new_img

    def button(self, img, x, y, w, h, text, color, action, fingers_touch, landmark,
               text_color=(0, 0, 0), text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1):
        self.rectangle(img, x, y, w, h, color)
        self.text(img, x + 10, y + h - 10, text, text_color,
                  text_fontFace=text_fontFace, text_fontScale=text_fontScale)
        if (fingers_touch[0] and (self.x + x <= landmark[4][0] <= self.x + x + w)
                and (self.y - self.win_h + y <= landmark[4][1] <= self.y - self.win_h + y + h)):
            if not self.pressed_button:
                self.pressed_button = True
                action()
        elif not fingers_touch[0]:
            self.pressed_button = False

    def add_img(self, img, x, y, img2):
        h1, w1, c1 = img.shape
        h2, w2, c2 = img2.shape
        img[self.y - self.win_h + y:self.y - self.win_h + y + h2, self.x + x:self.x + x + w2] = img2[max(0, -y):min(h2, h1 - y), max(0, -x):min(w2, w1 - x)]
