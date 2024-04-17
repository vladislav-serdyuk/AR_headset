"""
Copyright (C) 2024  Vladislav Serdyuk

Этот файл — часть AR_headset.
AR_headset — свободная программа: вы можете перераспространять ее и/или
изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
в каком она была опубликована Фондом свободного программного обеспечения;
либо версии 3 лицензии, либо любой более поздней версии.
Foobar распространяется в надежде, что она будет полезной, но БЕЗО ВСЯКИХ ГАРАНТИЙ;
даже без неявной гарантии ТОВАРНОГО ВИДА или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ.
Подробнее см. в Стандартной общественной лицензии GNU.
Вы должны были получить копию Стандартной общественной лицензии GNU вместе с этой программой.
Если это не так, см. <https://www.gnu.org/licenses/>.
"""

import os

import numpy as np
import cv2
import sounddevice as sd
import soundfile as sf

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self):
        super().__init__()
        self.win_h = 200
        self.win_w = 400
        self.name = 'Audio player'
        self.audio_formats = ['mp3', 'wav']
        audio_files = []
        for file in os.listdir('audio'):
            if file.rsplit('.', 1)[1] in self.audio_formats:
                audio_files.append(file)
        self.audio_files = audio_files
        self.select = ''
        self.is_play = False

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer: list):
        super().__call__(img, fingers_up, fingers_touch, landmark, buffer)
        if self.hide:
            return

        for i, file in enumerate(self.audio_files):
            self.button(img, 0, i * 40, 200, 35, file, (200, 255, 200),
                        lambda f=file: self.set_select(f), fingers_touch, landmark)

        self.text(img, 210, 30, self.select, (0, 0, 0))

        if self.is_play:
            self.button(img, 200, self.win_h-35, 200, 35, 'Stop', (0, 0, 255),
                        lambda: self.stop(), fingers_touch, landmark)
        else:
            self.button(img, 200, self.win_h - 35, 200, 35, 'Play', (0, 255, 0),
                        lambda: self.play(), fingers_touch, landmark)

    def set_select(self, file):
        self.select = file

    def play(self):
        if self.select == '':
            return
        self.is_play = True
        data, fs = sf.read('audio/' + self.select)
        sd.play(data, fs, loop=True)

    def stop(self):
        sd.stop()
        self.is_play = False
