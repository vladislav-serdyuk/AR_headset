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

from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.windows_height = 220
        self.window_width = 580
        self.name = 'Клавиатура'
        self.layout = 'en'

    def __call__(self, img):
        super().__call__(img)
        if self.hide:
            return

        keys_en = [
            '1234567890+-=',
            'qwertyuiop[]|',
            'asdfghjkl;:\'\n',
            'zxcvbnm.,<>/?',
        ]

        keys_ru = [
            '1234567890()@',
            'йцукенгшщзхъ\\',
            'фывапролджэ"\n',
            'ячсмитьбю.,,?',
        ]

        keys_spec = [
            '`~!@#$%^&*()_',
            '№-+*/',
            ':;\'"',
            '.,<>?/\\|',
        ]

        keys = {
            'en': keys_en,
            'ru': keys_ru,
            'spec': keys_spec
        }[self.layout]

        for y, row in enumerate(keys):
            for x, c in enumerate(row):
                self.button(img, x * 45, y * 45, 40, 40, c, (200, 0, 0),
                            lambda k=c: self.write_char_to_buffer(k))

        self.button(img, 0, 180, self.window_width - 105, 40, '', (200, 0, 0), lambda: self.write_char_to_buffer(' '))
        self.button(img, self.window_width - 100, 180, 100, 40, 'en/ru', (200, 0, 0), self.change_layout)

    def change_layout(self):
        if self.layout == 'en':
            self.layout = 'ru'
        elif self.layout == 'ru':
            self.layout = 'spec'
        elif self.layout == 'spec':
            self.layout = 'en'
