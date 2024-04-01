import numpy as np
import cv2

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
                        img[max(min(self.y - self.win_h + i, h - 1), 0)][max(min(self.x + j, w - 1), 0)] = (0, 0, 0)

    def clean(self):
        self.art = np.zeros((self.win_w, self.win_h))
