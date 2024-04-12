# AR_headset
![img](https://github.com/vladislav-serdyuk/AR_headset/blob/main/docs/GUI_exemple.png)
## Важно
Библиотека opencv-python ver: 4.9.0.80 имеет дыру безопасности (CVE-2019-9423)
## Для пользователей
### Настройка
- Установите зависимости (pip install -r requirements.txt)
- Измените templates/index.html | div > img > width так, чтобы растояние между картинками было равна 6см

### Использавание
#### Часы
Вытените указ. палец в часы часть, чтобы передвинуть

Зажмите большой с средним, чтобы изменить тип

#### Окна
Зажмите большой с указательным, чтобы передвигать

Зажмите большой с указательным, чтобы свернуть

#### Кнопки
Нажатие - зажмите большой с указательным

#### Paint
Зажмите большой с указательным, чтобы рисовать

Зажмите большой с указательным в краном квадрате, чтобы стиреть

#### Timer
h = часы

m = минуты

#### Пакеты
Используйте pkgmgr.py

Сначала введите
i - install, d - delete, q - quit

Потом Имя файла/Имя пакета

## Для Разрабов
### Назачение файлов
main.py: оснавной файл

GUIlib.py: Библиотека GUI

GUImgr.py: инициализация пакетов и отрисовка

pkglist.json: хранит данные пакетов

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
show_window = True
# end

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

    def __call__(self, img: np.ndarray, fingers_up: list[int], fingers_touch: list[int], landmark: list[list[int]],
                 buffer: list[str]): ...  # track finger


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

    def __call__(self, img: np.ndarray, fingers_up: list[int], fingers_touch: list[int], landmark: list[list[int]],
                 buffer: list[str]): ...

    def rectangle(self, img, x, y, w, h, color, radius=10, thickness=-1, line_type=cv2.LINE_AA): ...

    def text(self, img, x, y, text, color, text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1): ...

    def button(self, img, x, y, w, h, text, color, action, fingers_touch, landmark,
               text_color=(0, 0, 0), text_fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, text_fontScale=1): ...

    def add_img(self, img, x, y, img2): ...

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
Упакуйте в zip
