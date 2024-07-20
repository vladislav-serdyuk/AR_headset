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
from pkg.videoplayer.videoplayer_module import VideoPlayer


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.windows_height = 340
        self.window_width = 250
        self.name = 'ВидеоПлейер'
        self.video_formats = ['mp4', 'avi', 'mov', 'mpg', 'wmv']
        video_files = []
        for file in os.listdir('video'):
            if file.rsplit('.', 1)[1] in self.video_formats:
                video_files.append(file)
        self.video_files = video_files
        self.select = ''
        self.is_play = False
        # self.video: None | cv2.VideoCapture = None
        # self.new_time = time.time()
        self.frame = None
        # self.player: MediaPlayer | None = None
        self.player: VideoPlayer | None = None

    def __call__(self, img):
        super().__call__(img)
        # if self.is_play and time.time() >= self.new_time:
            # fps = self.video.get(cv2.CAP_PROP_FPS)
            # self.new_time += 1 / fps
            # ret, frame = self.video.read()
            # while time.time() >= self.new_time:
            #     self.new_time += 1 / fps
            #     ret, frame = self.video.read()
            # if not ret:
            #     self.stop()
            # else:
            #     h, w, c = frame.shape
            #     new_h = self.windows_height - 35
            #     new_w = w * new_h // h
            #     self.window_width = new_w
            #     self.frame = cv2.resize(frame, dsize=(new_w, new_h))
        if self.is_play:
            frame = self.player.get_frame()
            if frame is not None:
                h, w, c = frame.shape
                new_h = self.windows_height - 35
                new_w = w * new_h // h
                self.window_width = new_w
                self.frame = cv2.resize(frame, dsize=(new_w, new_h))

        if self.hide:
            return

        if self.is_play:
            pass
        else:
            for i, file in enumerate(self.video_files):
                self.button(img, 5, i * 35 + 5, self.window_width - 10, 30, file, (200, 255, 200),
                            lambda f=file: self.set_select(f))
            self.text(img, 10, self.windows_height - 60, self.select, (0, 0, 0))

        if self.is_play:
            self.button(img, self.window_width // 2 + 5, self.windows_height - 35, self.window_width // 2 - 10, 35,
                        'Стоп', (0, 0, 255),
                        lambda: self.stop())
            if self.player.get_pause():
                self.button(img, 5, self.windows_height - 35, self.window_width // 2 - 10, 35,
                            'Продолжить', (0, 255, 0),
                            lambda: self.pause_to_play())
            else:
                self.button(img, 5, self.windows_height - 35, self.window_width // 2 - 10, 35,
                            'Пауза', (255, 0, 0),
                            lambda: self.pause())
            if self.frame is not None:
                self.add_img(img, 0, 0, self.frame)
        else:
            self.button(img, 5, self.windows_height - 35, self.window_width - 10, 35, 'Старт', (0, 255, 0),
                        lambda: self.play())

    def set_select(self, file):
        self.select = file

    def play(self):
        if self.select == '':
            return
        self.is_play = True
        self.player = VideoPlayer(f'video/{self.select}')
        # self.video = cv2.VideoCapture(f'video/{self.select}')
        # self.player = MediaPlayer(f'video/{self.select}')
        # self.new_time = time.time()

    def stop(self):
        self.is_play = False
        # self.player.close_player()
        self.player.stop()
        self.window_width = 250

    def pause(self):
        self.player.pause()

    def pause_to_play(self):
        self.player.play()
