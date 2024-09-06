from GUIlib import WindowGUI


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.name = 'Browser'
        self.windows_height = 100
        self.window_width = 210
        self.x = 200
        self.y = 400

    def __call__(self, img):
        super().__call__(img)
        if self.hide:
            return
        ...
