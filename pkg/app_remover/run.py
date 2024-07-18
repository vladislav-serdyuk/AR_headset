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

from json import JSONDecoder
import threading

from GUIlib import WindowGUI
import pkgmgr

json_decoder = JSONDecoder()


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.name = 'App remover'  # имя окна
        self.windows_height = 300  # высота окна
        self.window_width = 560  # ширина окна
        self.x = 200  # координаты нижнего левого угла
        self.y = 400
        self.pkg_list: dict[str, dict[str, str]] = {}
        self.cur_pkg: str | None = None
        self.delete_status = ''
        self.ignore_pkgs_list = ['sys_app_menu', 'app_installer', 'app_remover']

        self.refresh()

    def __call__(self, img):
        super().__call__(img)  # прорисовка и обработка окна
        if self.hide:
            return
        if self.pkg_list is not None:
            for i, (name, value) in enumerate(self.pkg_list.items()):
                x = i % 3 * 185 + 5
                y = i // 3 * 35 + 5
                self.button(img, x, y, 180, 30, value['info'], (220, 255, 0),
                            lambda: self.select(name), text_font_scale=0.9)
        # self.button(img, 5, self.windows_height - 45, 200, 40, 'refresh', (200, 200, 200), self.refresh)

        if self.cur_pkg is not None:
            self.text(img, 5, self.windows_height - 20, self.pkg_list[self.cur_pkg]['info'], (0, 0, 0))
            if self.delete_status == '':
                self.button(img, 180, self.windows_height - 40, 100, 35, 'Delete', (0, 0, 255), self.start_delete_pkg)
            else:
                self.text(img, 200, self.windows_height - 20, self.delete_status, (0, 0, 255))

    def select(self, pkg: str):
        self.cur_pkg = pkg

    def start_delete_pkg(self):
        self.delete_status = 'deleting'
        threading.Thread(target=self.delete, daemon=True).start()

    def delete(self):
        pkgmgr.delete_pkg(self.cur_pkg)
        self.delete_status = ''
        self.send_message('reload-apps')

    def refresh(self):
        with open('pkglist.json') as file:
            self.pkg_list = JSONDecoder().decode(file.read())
        for ign_pkg in self.ignore_pkgs_list:
            if ign_pkg in self.pkg_list:
                del self.pkg_list[ign_pkg]
