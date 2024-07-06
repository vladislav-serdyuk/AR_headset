# Для Разработчиков
## Назначение файлов
main.py: основной файл

GUIlib.py: GUI framework

pkglist.json: хранит данные пакетов

templates/index.html: страница трансляции

templates/script.js: скрипт

pkg/pkg_name/: папка пакета pkg_name

pkg/pkg_name/run.py: главный файл пакета pkg_name

### Структура pkglist.json
```json
{
  "pkg1_name": {
    "dir": "pkg1_folder",
    "info": "pkg1_window_name"
  },
  "pkg2_name": {
    "dir": "pkg2_folder",
    "info": "pkg2_window_name"
  }
}
```

## Создание пакета
Допустим вы хотите создать приложение.

Создайте ./files/run.py 

Пример для оконного приложения:
```python
from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.hide = True  # является ли окно свёрнутым
        self.background_color = (255, 255, 255)  # цвет фона
        self.name = 'window'  # имя окна
        self.title_color = (0, 0, 0)  # цвет заголовка
        self.windows_height = 100  # высота окна
        self.window_width = 210  # ширина окна
        self.x = 200  # координаты нижнего левого угла
        self.y = 400
        # необязательно указывать все параметры
        # здесь показаны значения по умолчанию

    def __call__(self, img):
        """
        Этот метод вызывается постоянно
        """
        super().__call__(img)  # прорисовка и обработка окна
        if self.hide:
            return
        ...
```

Пример для виджета:
```python
from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.height_moving_area = 50  # размер области захвата
        self.width_moving_area = 50
        self.x = 10  # координата верхнего левого угла области захвата
        self.y = 10
        self.name = 'base gui'  # имя виджета
        # необязательно указывать все параметры
        # здесь показаны значения по умолчанию

    def __call__(self, img):
        """
        Этот метод вызывается постоянно
        """
        super().__call__(img)  # обработка перемещения
        ...
```
Для дальнейшего создания приложения используйте [GUI app framework](GUI_app_framework.md)

Доп файлы пихайте в ./files/

Создайте ./pkg_data.json:
```json
{
  "name": "my_pkg",
  "dir": "myPkg",
  "info": "My App"
}
```
    pkg_data["info"] = self.name
"dir" - папка установки пакета

Упакуйте **содержимое** (./*) в zip (**не папку!!!**)
