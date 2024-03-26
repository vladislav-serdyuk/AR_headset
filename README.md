# AR_headset
## Для пользователей
### Настройка
- Установите зависимости (pip install -r requirements.txt)
- Измените templates/index.html | div > img > width под экран

### Использавание
#### Часы
Вытените указ. палец в часы часть чтобы передвинуть
Зажмите большой с средним чтобы изменить тип

#### Окна
Вытените указ. палец в верхнию часть чтобы передвинуть
Вытените указ. палец в верхнию правуючасть часть чтобы сверныть

#### Paint
Зажмите большой с указательным чтобы рисовать
Зажмите большой с указательным в краном квадрате чтобы стиреть

#### Пакеты
Используйте pkgmgr.py

i, d, q

## Для Разрабов
### Архетиктура
main.py: оснавной файл
GUIlib.py: Библиотека GUI
GUImgr.py: инициализация пакетов и отрисовка
pkglist.json: хранит мета данные пакетов
templates/index.html: страница трансляции
templates/script.js: скрипт
pkg/pkg_name/: папка пакета pkg_name
pkg/pkg_name/run.py: главный файл пакета pkg_name

#### Структура pkglist.json
```
{
  "pkg1_name": {
    "dir": "pkg1_folder"
  },
  "pkg2_name": {
    "dir": "pkg2_folder"
  }
}
```

### Функции  и методы
#### main.py
```
def process_image(frame: np.ndarray) -> np.ndarray: ...

@app.route('/')
def index() -> str: ...


@app.route('/video_feed')
def video_feed() -> Response: ...


@app.route('/script.js')
def script() -> str: ...


def get_frame() -> Generator[bytes, Any, None]:
    """
    Получает изображение с камеры, обрабатывает, отправляет клиенту
    :return: Generator[bytes, Any, None]
    """
    ...

# setting
debug = True
hand_on_gui = True
flip_img = False
show_window = True
# end

```
#### GUImgr.py
```
def init_gui(): ...


def draw_gui(img: np.ndarray, fingers_up: list[int], fingers_touch: list[int], landmark: list[list[int]]): ...

```
#### GUIlib.py
```
import cv2
import numpy as np


class GUI:
    def __init__(self):  # setup position
        self.h = 50
        self.w = 50
        self.x = 10
        self.y = 10
        self.track = False

    def __call__(self, img, fingers_up, fingers_touch, landmark): ...  # track finger


class WindowGUI(GUI):
    def __init__(self):
        super().__init__()
        self.hide = True
        self.background_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.border_thickness = 2
        self.name = 'window'
        self.title_h = 30
        self.title_color = (0, 0, 0)
        self.win_h = 100
        self.win_w = 210
        self.h = self.title_h
        self.w = self.win_w - 50
        self.x = 200
        self.y = 200
        self.t_pre = 0

    def __call__(self, img, fingers_up, fingers_touch, landmark): ...

    def rectangle(self, img, x, y, w, h, color, border_color=None): ...

    def text(self, img, x, y, text, color, text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1): ...

    def button(self, img, x, y, w, h, text, color,  action, fingers_touch, landmark, border_color=None,
               text_color=(0, 0, 0), text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1): ...

    @staticmethod
    def add_img(img, x, y, img2):

```

### Создание пакета
Создайте:

```
folder
|   pkg_data.json
|
\---files
        run.py
```

pkg_data.json:
```
{
  "name": "my_pkg",
  "dir": "myPkg",
  "info": "This is My Pkg"
}
```
