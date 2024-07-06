# GUI_app_framework
## GUI
```python
class GUI: ...
```
    Класс для создания простого GUI объекта

### GUI._\_init__()
```python
class GUI:
    def __init__(self,
                 fingers_up: list[int],
                 fingers_touch: list[int],
                 buffer: list[str],
                 message: list[str],
                 landmark: list[list[int]]
                 ):
        self.buffer = buffer
        self.message = message
        self.fingers_up = fingers_up
        self.fingers_touch = fingers_touch
        self.landmark = landmark
```
    buffer: буфер символов виртуальной клавиатуры
    message[0]: переменная для отправки сообщений
        start:{app.name} открывает app
        window-top:{app.id} переставляет окно app на передний план
    fingers_up: какие пальцы не согнуты (пример [0, 1, 0, 0, 1]: указательный и мизинец)
    fingers_touch: какие пальцы соприкасаются с большим (пример [1, 0, 0, 1]: указательный с большим)
    landmark: позиции основных точек на ладони (подробнее в документации MediaPipe)

### GUI._\_call__()
```python
class GUI:
    def __call__(self,
                 img: np.ndarray
                 ): ...
```
### GUI.write_char_to_buffer()
```python
class GUI:
    def write_char_to_buffer(self,
                             char: str
                             ): ...
```
### GUI.read_char_from_buffer()
```python
class GUI:
    def read_char_from_buffer(self): ...
```
### GUI.send_message()
```python
class GUI:
    def send_message(self,
                     message): ...
```
### GUI.read_message()
```python
class GUI:
    def read_message(self): ...
```
### GUI.set_message_as_read()
```python
class GUI:
    def set_message_as_read(self): ...
```
    set_message_as_read() = send_message('')

## WindowGUI
```python
class WindowGUI(GUI): ...
```
    Класс для создания оконного приложения

### WindowGUI._\_init__()
```python
class WindowGUI(GUI):
    def __init__(self,
                 fingers_up: list[int],
                 fingers_touch: list[int],
                 buffer: list[str],
                 message: list[str],
                 landmark: list[list[int]]
                 ):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        ...
```

### WindowGUI._\_call__()
```python
class WindowGUI(GUI):
    def __call__(self,
                 img: np.ndarray
                 ): ...
```
    Отвечает за окно

### WindowGUI.rectangle()
```python
class WindowGUI(GUI):
    def rectangle(self,
                  img: np.ndarray,
                  x: int,
                  y: int,
                  w: int,
                  h: int,
                  color: tuple[int, int, int],
                  radius=10,
                  thickness=-1,
                  line_type=cv2.LINE_AA
                  ): ...
```
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

### WindowGUI.text()
```python
class WindowGUI(GUI):
    def text(self,
             img: np.ndarray,
             x: int,
             y: int,
             text: str,
             color: tuple[int, int, int],
             text_font_face=cv2.FONT_HERSHEY_COMPLEX_SMALL,
             text_font_scale=1
             ): ...
```
    Рисует текст
    :param img: где рисовать
    :param x: x координата нижней левой точки
    :param y: y координата нижней левой точки
    :param text: текст
    :param color: цвет текста
    :param text_font_face: шрифт текста
    :param text_font_scale: размер текста

### WindowGUI.button()
```python
class WindowGUI(GUI):
    def button(self,
               img: np.ndarray,
               x: int,
               y: int,
               w: int,
               h: int,
               text: str,
               color: tuple[int, int, int],
               action: typing.Callable[[], None],
               text_color=(0, 0, 0),
               text_font_face=cv2.FONT_HERSHEY_COMPLEX_SMALL,
               text_font_scale=1
               ): ...
```
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

### WindowGUI.add_img()
```python
    class WindowGUI(GUI):
        def add_img(self,
                    img: np.ndarray,
                    x: int,
                    y: int,
                    img2: np.ndarray): ...
```
    Добавляет изображение
    :param img: куда добавлять
    :param x: x координата верхний правой точки
    :param y: y координата верхний правой точки
    :param img2: Что добавлять

## Пример приложения
```python
from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)  # инициализация приложения
        self.windows_height = 215  # высота окна
        self.window_width = 175  # ширина окна
        self.name = 'Calculator'  # имя окна
        self.expression = ''  # выражение для вычисления

    def __call__(self, img):  # этот метод вызывается циклично
        # img: np.array() - изображение где будет рисоваться окно
        super().__call__(img)  # это очень нужная строчка, она рисует окно и обрабатывает его сворачивание
        if self.hide:  # если окно свёрнуто, то пропускаем всё что идёт дальше
            return

        # рисуем прямоугольник, где будет результат
        self.rectangle(img,  # передаём изображение где будет рисоваться прямоугольник
                       0,  # x координата верхнего левого угла
                       0,  # y координата верхнего левого угла
                       self.window_width,  # ширина прямоугольника
                       40,  # высота прямоугольник
                       (255, 255, 255)  # цвет прямоугольника (BGR)
                       )
        # добавляем текст
        self.text(img,
                  10,  # x координата нижнего левого угла
                  30,  # y координата нижнего левого угла
                  self.expression,  # текст 
                  (0, 0, 0)  # цвет (BGR)
                  )

        keys = [  # кнопки на калькуляторе
            '123+',
            '456-',
            '789/',
            'c0=*',
        ]

        for y, row in enumerate(keys):
            for x, c in enumerate(row):
                self.button(img,
                            x * 45,  # x координата верхнего левого угла
                            40 + y * 45,  # y координата верхнего левого угла
                            40,  # ширина
                            40,  # высота
                            c,  # текст
                            (0, 0, 230),  # цвет
                            lambda k=c: self.calc(k)  # функция
                            )

    def calc(self, x):
        if x == 'c':
            self.expression = ''
        elif x == '=':
            try:
                self.expression = str(eval(self.expression))
            except SyntaxError:
                pass
            except ZeroDivisionError:
                pass
        else:
            self.expression += x

```
