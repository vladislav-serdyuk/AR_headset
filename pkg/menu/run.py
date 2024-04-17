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

import json

import numpy as np
import cv2

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self):
        super().__init__()
        self.x = 50
        self.y = 130
        self.win_h = 0
        self.win_w = 0
        self.name = 'Menu'
        self.apps = []
        with open('pkglist.json') as file:
            pkg_list: dict = json.JSONDecoder().decode(file.read())
        for app in pkg_list.values():
            name = app["info"]
            if name not in ['Menu', 'Clock']:
                self.apps.append(name)

    def __call__(self, img, fingers_up, fingers_touch, landmark, buffer: list):
        if fingers_up == [0, 1, 0, 0, 1]:
            self.hide = False
        if self.hide:
            return
        for i, app in enumerate(self.apps):
            x = i % 3 * 180
            y = i // 3 * 40
            self.button(img, x, y, 170, 30, app, (255, 200, 150), lambda a=app: self.open(buffer, a),
                        fingers_touch, landmark)

    def open(self, buffer: list, app):
        buffer.append(f'open:{app}')
        self.hide = True
