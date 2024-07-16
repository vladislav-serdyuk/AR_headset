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

import os
import time

import cv2
from ffpyplayer.player import MediaPlayer

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.windows_height = 340
        self.window_width = 250
        self.name = 'Video player'
        self.video_formats = ['mp4']
        video_files = []
        for file in os.listdir('video'):
            if file.rsplit('.', 1)[1] in self.video_formats:
                video_files.append(file)
        self.video_files = video_files
        self.select = ''
        self.is_play = False
        self.video: None | cv2.VideoCapture = None
        self.new_time = time.time()
        self.frame = None
        self.player = None

    def __call__(self, img):
        super().__call__(img)
        if self.is_play and time.time() >= self.new_time:
            fps = self.video.get(cv2.CAP_PROP_FPS)
            self.new_time += 1 / fps
            ret, frame = self.video.read()
            if not ret:
                self.stop()
            else:
                h, w, c = frame.shape
                self.frame = cv2.resize(frame, dsize=(w * (self.windows_height + self.height_moving_area) // h,
                                                      self.windows_height + self.height_moving_area))

        if self.hide:
            return

        for i, file in enumerate(self.video_files):
            self.button(img, 5, i * 35 + 5, self.window_width - 10, 30, file, (200, 255, 200),
                        lambda f=file: self.set_select(f))

        self.text(img, 10, self.windows_height - 60, self.select, (0, 0, 0))

        if self.is_play:
            self.button(img, 5, self.windows_height - 35, self.window_width - 10, 35, 'Stop', (0, 0, 255),
                        lambda: self.stop())
            self.add_img(img, self.window_width + 5, 0, self.frame)
        else:
            self.button(img, 5, self.windows_height - 35, self.window_width - 10, 35, 'Play', (0, 255, 0),
                        lambda: self.play())

    def set_select(self, file):
        self.select = file

    def play(self):
        if self.select == '':
            return
        self.is_play = True
        self.video = cv2.VideoCapture(f'video/{self.select}')
        self.player = MediaPlayer(f'video/{self.select}')
        self.new_time = time.time()

    def stop(self):
        self.is_play = False
        self.player.close_player()
