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
import base64
import wget
import threading
import random

from GUIlib import WindowGUI
import pkgmgr
import os

from github import Github
from github.GithubException import UnknownObjectException

json_decoder = JSONDecoder()


def get_pkg_list():
    pkg_list = []
    with Github() as gh:
        repo = gh.get_repo('vladislav-serdyuk/AR_headset_pkgs')
        contents = repo.get_contents('')
        for file_content in contents:
            if file_content.type == 'file':
                continue
            # zip_file = None
            for pkg_file_content in repo.get_contents(file_content.path):
                if pkg_file_content.path.endswith('.zip'):
                    zip_file = pkg_file_content
                    break
            else:
                continue
            try:
                pkg_data_file = repo.get_contents(file_content.path + '/src/pkg_data.json')
            except UnknownObjectException:
                continue
            pkg_data_content = base64.b64decode(pkg_data_file.content.encode()).decode()
            pkg_data = json_decoder.decode(pkg_data_content)
            pkg = {'name': pkg_data['info'], 'description': pkg_data['description'], 'dir_on_github': file_content.path,
                   'zip_file': zip_file.path, 'download_size': zip_file.size, 'install_size': None}
            pkg_list.append(pkg)
    return pkg_list


def convert_to_kb_mb_gb(num, _round=2):
    ed = ['B', 'KB', 'MB', 'GB']
    cnt = 0
    while num >= 1000 and cnt < len(ed):
        num = round(num / 1000, _round)
        cnt += 1
    if _round == 0:
        num = int(num)
    return f'{num}{ed[cnt]}'


class App(WindowGUI):
    def __init__(self, fingers_up: list[int], fingers_touch: list[int],
                 buffer: list[str], message: list[str], landmark: list[list[int]]):
        super().__init__(fingers_up, fingers_touch, buffer, message, landmark)
        self.name = 'Установщик'  # имя окна
        self.windows_height = 420  # высота окна
        self.window_width = 460  # ширина окна
        self.x = 200  # координаты нижнего левого угла
        self.y = 400
        self.pkg_list = None
        self.cur_pkg = None
        self.install_status = ''
        self.refresh_status = ''

    def __call__(self, img):
        super().__call__(img)  # прорисовка и обработка окна
        if self.hide:
            return
        if self.pkg_list is not None:
            for i, item in enumerate(self.pkg_list):
                self.button(img, 5, i * 30 + 5, 200, 25, item['name'], (220, 255, 0),
                            lambda: self.select(item), text_font_scale=0.6)
        if self.refresh_status == '':
            self.button(img, 5, self.windows_height - 35, 200, 30, 'Обновить данн', (200, 200, 200),
                        self.refresh)
        else:
            self.text(img, 10, self.windows_height - 20, self.refresh_status, (50, 50, 50))

        if self.cur_pkg is not None:
            self.text(img, 240, 35, self.cur_pkg['name'], (0, 0, 0))

            self.text(img, 220, 70, 'Информация:', (0, 0, 0))
            description_word = self.cur_pkg['description'].split()
            line = ''
            line_num = 0
            for word in description_word:
                if len(line) + len(word) < 18 or (line == '' and len(word) >= 18):
                    line += word + ' '
                else:
                    self.text(img, 220, 110 + line_num * 30, line, (0, 0, 0))
                    line = ''
                    line_num += 1
            self.text(img, 220, 110 + line_num * 30, line, (0, 0, 0))
            self.text(img, 215, self.windows_height - 60,
                      f'Размер скч:{convert_to_kb_mb_gb(self.cur_pkg["download_size"], 1)}',
                      (0, 0, 0),
                      text_font_scale=0.6)
            if self.install_status == '':
                self.button(img, 215, self.windows_height - 45, 240, 40, 'Установить', (0, 255, 0), self.start_install_pkg)
            else:
                self.text(img, 220, self.windows_height - 20, self.install_status, (0, 0, 255))

    def select(self, pkg):
        self.cur_pkg = pkg

    def refresh(self):
        self.refresh_status = 'Обновление списка'
        threading.Thread(target=self.refresh_in_bg).start()

    def refresh_in_bg(self):
        self.pkg_list = get_pkg_list()
        # print(self.pkg_list)
        # for i in range(500_000_000):
        #     ...
        # self.pkg_list = [
        #     {'name': 'App installer', 'description': 'Apps installer', 'dir_on_github': 'App installer',
        #      'zip_file': 'App installer/App installer.zip', 'download_size': 2801, 'install_size': None},
        #     {'name': 'App remover', 'description': 'Apps remover', 'dir_on_github': 'App remover',
        #      'zip_file': 'App remover/App remover.zip', 'download_size': 1847, 'install_size': None},
        #     {'name': 'Audio player', 'description': 'Audio player', 'dir_on_github': 'Audio player',
        #      'zip_file': 'Audio player/Audio player.zip', 'download_size': 1604, 'install_size': None},
        #     {'name': 'Calc Pro', 'description': 'Improved version of the calculator', 'dir_on_github': 'Calc Pro',
        #      'zip_file': 'Calc Pro/Calc Pro.zip', 'download_size': 1683, 'install_size': None},
        #     {'name': 'Calculator', 'description': 'Simple calculator', 'dir_on_github': 'Calculator',
        #      'zip_file': 'Calculator/Calculator.zip', 'download_size': 1515, 'install_size': None},
        #     {'name': 'Keyboard', 'description': 'Print text in AR', 'dir_on_github': 'Keyboard',
        #      'zip_file': 'Keyboard/Keyboard.zip', 'download_size': 1431, 'install_size': None},
        #     {'name': 'Paint', 'description': 'Art in AR', 'dir_on_github': 'Paint',
        #      'zip_file': 'Paint/Paint.zip', 'download_size': 1548, 'install_size': None},
        #     {'name': 'Timer', 'description': 'Timer', 'dir_on_github': 'Timer',
        #      'zip_file': 'Timer/Timer.zip', 'download_size': 37039, 'install_size': None},
        #     {'name': 'Video player', 'description': 'Video player', 'dir_on_github': 'Video player',
        #      'zip_file': 'Video player/Video player.zip', 'download_size': 1831, 'install_size': None},
        #     {'name': '_Clock', 'description': 'Clock widget', 'dir_on_github': '_Clock',
        #      'zip_file': '_Clock/_Clock.zip', 'download_size': 1692, 'install_size': None},
        #     {'name': '_Menu', 'description': 'Main apps menu', 'dir_on_github': '_Menu',
        #      'zip_file': '_Menu/_Menu.zip', 'download_size': 1572, 'install_size': None}
        # ]
        self.refresh_status = ''

    def start_install_pkg(self):
        self.install_status = 'preparing to downloading'
        threading.Thread(target=self.install, daemon=True).start()

    def install(self):
        url = f'https://raw.githubusercontent.com/vladislav-serdyuk/AR_headset_pkgs/main/{self.cur_pkg["zip_file"]}'
        # url = f'http://speedtest.ftp.otenet.gr/files/test10Mb.db'
        print(f'downloading {url.replace(" ", "%20")}')
        random_number = random.randint(1, 1_000_000_000)
        wget.download(url, f'pkg_for_install_{random_number}.zip', self.download_tracker)
        self.install_status = 'install'
        print('install pkg')
        pkgmgr.install_pkg(f'pkg_for_install_{random_number}.zip', skip_question=True)
        self.install_status = 'cleanup'
        print(f'deleted pkg_for_install_{random_number}.zip')
        os.remove(f'pkg_for_install_{random_number}.zip')
        self.install_status = ''
        self.send_message('reload-apps')

    def download_tracker(self, current, total, wight):
        self.install_status = \
            f'{round(current / total * 100, 1)}% ({convert_to_kb_mb_gb(current, 1)}/{convert_to_kb_mb_gb(total, 1)})'
