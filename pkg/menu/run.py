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

import json

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.x = 40
        self.y = 130
        self.windows_height = 0
        self.window_width = 0
        self.name = '_Menu'
        self.apps = []
        with open('pkglist.json', encoding="utf-8") as file:
            pkg_list: dict = json.JSONDecoder().decode(file.read())
        for app in pkg_list.values():
            name = app["info"]
            if name[0] != '_':
                self.apps.append(name)

    def __call__(self, img):
        if self.fingers_up == [0, 1, 0, 0, 1]:
            self.message[0] = f'window-top:{self.id}'
            self.hide = False
        if self.hide:
            return
        self.button(img, 440, -40, 120, 30, 'Закрыть', (0, 0, 200), self.close)
        for i, app in enumerate(self.apps):
            x = i % 3 * 190
            y = i // 3 * 40
            self.button(img, x, y, 180, 30, app, (255, 200, 150), lambda a=app: self.open(self.message, a))

    def open(self, message: list, app):
        message[0] = f'open:{app}'
        self.hide = True

    def close(self):
        self.hide = True
