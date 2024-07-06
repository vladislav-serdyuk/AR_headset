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

import typing

import cv2
import numpy as np

_pressed_button = False
_window_track = False


class GUI:
    """
    Класс для создания простого GUI объекта
    """

    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):  # setup position
        self.height_moving_area = 50
        self.width_moving_area = 50
        self.x = 10
        self.y = 10
        self._track = False
        self._track_x = 0
        self._track_y = 0
        self.name = 'base gui'
        self.id = id(self)
        self.buffer = buffer
        self.message = message
        self.fingers_up = fingers_up
        self.fingers_touch = fingers_touch
        self.landmark = landmark

    def __call__(self, img: np.ndarray):  # track finger
        if self.landmark[0] == (0, 0):
            return
        global _window_track
        if self.fingers_touch[0] == 0:
            self._track = False
            _window_track = False
        elif self._track:
            self.x = self.landmark[8][0] - self._track_x
            self.y = self.landmark[8][1] - self._track_y
        elif (not _window_track and self.x <= self.landmark[8][0] <= self.x + self.width_moving_area
              and self.y <= self.landmark[8][1] <= self.y + self.height_moving_area):
            self._track_x = self.landmark[8][0] - self.x
            self._track_y = self.landmark[8][1] - self.y
            self._track = True
            _window_track = True
            self.message[0] = f'window-top:{self.id}'

    def write_char_to_buffer(self, char: str):
        self.buffer.append(char)

    def read_char_from_buffer(self):
        return self.buffer.pop(0)

    def send_message(self, message):
        self.message[0] = message

    def read_message(self):
        return self.message[0]

    def set_message_as_read(self):
        self.message[0] = ''


class WindowGUI(GUI):
    """
    Класс для создания оконного приложения
    """

    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.hide = True  # является ли окно скрытым
        self.background_color = (255, 255, 255)
        self.name = 'window'  # имя окна
        self.title_color = (0, 0, 0)
        self.windows_height = 100
        self.window_width = 210
        self.height_moving_area = 30
        self.width_moving_area = self.window_width - 50
        self.x = 200  # координаты нижнего левого угла
        self.y = 400

    def __call__(self, img: np.ndarray):
        if self.hide:
            if self.read_message() == f'open:{self.name}':
                self.set_message_as_read()
                self.send_message(f'window-top:{self.id}')
                self.hide = False
        else:
            self.width_moving_area = self.window_width - 50
            if (self.x + self.width_moving_area <= self.landmark[8][0] <= self.x + self.window_width
                    and self.y <= self.landmark[8][1] <= self.y + self.height_moving_area and self.fingers_touch[0]):
                self.hide = True
            super().__call__(img)
            self.rectangle(img, 0, 0, self.window_width, self.windows_height + self.height_moving_area,
                           self.background_color)
            self.rectangle(img, 0, 0, self.window_width, self.windows_height, self.background_color)
            self.text(img, 10, self.windows_height + self.height_moving_area - 10, self.name, self.title_color)
            cv2.line(img, (self.x + self.width_moving_area + 15, self.y + self.height_moving_area // 2),
                     (self.x + self.width_moving_area + 35, self.y + self.height_moving_area // 2), (0, 0, 0, 220), 2)

    def rectangle(self, img: np.ndarray, x: int, y: int, w: int, h: int, color: tuple[int, int, int], radius=10,
                  thickness=-1, line_type=cv2.LINE_AA):
        """
        Рисует прямоугольник
        :param img: где рисовать
        :param x: x координата верхний правой точки
        :param y: y координата верхний правой точки
        :param w: ширина
        :param h: высота
        :param color: цвет
        :param radius: радиус закругления углов
        :param thickness: толщина линии (-1 == fill)
        :param line_type: тип линии
        :return:
        """

        #  corners:
        #  p1 - p2
        #  |     |
        #  p4 - p3

        color = color + (220,)

        top_left = (self.x + x, self.y - self.windows_height + y)
        bottom_right = (self.x + x + w, self.y - self.windows_height + y + h)
        p1 = top_left
        p2 = (bottom_right[0], top_left[1])
        p3 = bottom_right
        p4 = (top_left[0], bottom_right[1])

        overlay = img.copy()
        if thickness < 0:  # // draw rectangle
            cv2.rectangle(overlay, (p1[0] + radius, p1[1]), (p3[0] - radius, p3[1]), color, thickness, line_type)
            cv2.rectangle(overlay, (p1[0], p1[1] + radius), (p3[0], p3[1] - radius), color, thickness, line_type)
        else:  # // draw straight lines
            cv2.line(overlay, (p1[0] + radius, p1[1]), (p2[0] - radius, p2[1]), color, thickness, line_type)
            cv2.line(overlay, (p2[0], p2[1] + radius), (p3[0], p3[1] - radius), color, thickness, line_type)
            cv2.line(overlay, (p4[0] + radius, p4[1]), (p3[0] - radius, p3[1]), color, thickness, line_type)
            cv2.line(overlay, (p1[0], p1[1] + radius), (p4[0], p4[1] - radius), color, thickness, line_type)

        if radius > 0:  # // draw arcs
            cv2.ellipse(overlay, (p1[0] + radius, p1[1] + radius), (radius, radius), 180.0, 0, 90, color, thickness,
                        line_type)
            cv2.ellipse(overlay, (p2[0] - radius, p2[1] + radius), (radius, radius), 270.0, 0, 90, color, thickness,
                        line_type)
            cv2.ellipse(overlay, (p3[0] - radius, p3[1] - radius), (radius, radius), 0.0, 0, 90, color, thickness,
                        line_type)
            cv2.ellipse(overlay, (p4[0] + radius, p4[1] - radius), (radius, radius), 90.0, 0, 90, color, thickness,
                        line_type)

        img[:] = overlay

    def text(self, img: np.ndarray, x: int, y: int, text: str, color: tuple[int, int, int],
             text_font_face=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_font_scale=1):
        """
        Рисует текст
        :param img: где рисовать
        :param x: x координата нижней левой точки
        :param y: y координата нижней левой точки
        :param text: текст
        :param color: цвет текста
        :param text_font_face: шрифт текста
        :param text_font_scale: размер текста
        :return:
        """
        color = color + (240,)
        overlay = img.copy()
        cv2.putText(overlay, text, (self.x + x, self.y - self.windows_height + y), text_font_face, text_font_scale,
                    color)
        img[:] = overlay

    def button(self, img: np.ndarray, x: int, y: int, w: int, h: int, text: str, color: tuple[int, int, int],
               action: typing.Callable[[], None], text_color=(0, 0, 0), text_font_face=cv2.FONT_HERSHEY_COMPLEX_SMALL,
               text_font_scale=1):
        fingers_touch = self.fingers_touch
        landmark = self.landmark
        """
        Рисует кнопку
        :param img: где рисовать
        :param x: x координата верхний левой точки
        :param y: y координата верхний левой точки
        :param w: ширина
        :param h: высота
        :param text: текст
        :param color: цвет фона
        :param action: действие при нажатии (функция)
        :param text_color: цвет текста
        :param text_font_face: шрифт текста
        :param text_font_scale: размер текста
        :return:
        """
        global _pressed_button
        self.rectangle(img, x, y, w, h, color)
        self.text(img, x + 10, y + h - 10, text, text_color, text_font_face=text_font_face,
                  text_font_scale=text_font_scale)
        if not fingers_touch[0]:
            _pressed_button = False
        elif (not _pressed_button and (self.x + x <= landmark[4][0] <= self.x + x + w)
              and (self.y - self.windows_height + y <= landmark[4][1] <= self.y - self.windows_height + y + h)):
            _pressed_button = True
            action()

    def add_img(self, img: np.ndarray, x: int, y: int, img2: np.ndarray):
        """
        Добавляет изображение
        :param img: куда добавлять
        :param x: x координата верхний правой точки
        :param y: y координата верхний правой точки
        :param img2: Что добавлять
        :return:
        """
        h1, w1, c1 = img.shape
        h2, w2, c2 = img2.shape
        abs_x = self.x + x
        abs_y = self.y - self.windows_height + y
        img[max(0, abs_y):abs_y + h2, max(0, abs_x):abs_x + w2, :3] \
            = img2[max(0, -abs_y):h1 - abs_y, max(0, -abs_x):w1 - abs_x]
        h, w, c = img[max(0, abs_y):abs_y + h2, max(0, abs_x):abs_x + w2, :3].shape
        img[max(0, abs_y):abs_y + h2, max(0, abs_x):abs_x + w2, 3] \
            = np.ones((h, w), dtype=np.uint8) * 255
