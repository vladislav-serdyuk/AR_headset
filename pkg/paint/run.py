import numpy as np
import cv2

from GUIlib import WindowGUI


class App(WindowGUI):
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
