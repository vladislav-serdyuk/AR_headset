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

import sounddevice as sd
import soundfile as sf

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.windows_height = 340
        self.window_width = 430
        self.name = 'АудиоПлейер'
        self.audio_formats = ['mp3', 'wav', 'flac', 'ogg']
        audio_files = []
        for file in os.listdir('audio'):
            if file.rsplit('.', 1)[1] in self.audio_formats:
                audio_files.append(file)
        self.audio_files = audio_files
        self.select = ''
        self.is_play = False

    def __call__(self, img):
        super().__call__(img)
        if self.hide:
            return

        for i, file in enumerate(self.audio_files):
            self.button(img, 5, i * 35 + 5, 200, 30, file, (200, 255, 200), lambda f=file: self.set_select(f))

        self.text(img, 210, 30, self.select, (0, 0, 0))

        if self.is_play:
            self.button(img, 200, self.windows_height - 35, 225, 35, 'Стоп', (0, 0, 255), lambda: self.stop())
        else:
            self.button(img, 200, self.windows_height - 35, 225, 35, 'Старт', (0, 255, 0), lambda: self.play())

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
