"""
Этот файл — часть AR_headset.
AR_headset — свободная программа: вы можете перераспространять ее и/или
изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
в каком она была опубликована Фондом свободного программного обеспечения;
либо версии 3 лицензии, либо любой более поздней версии.
Foobar распространяется в надежде, что она будет полезной, но БЕЗО ВСЯКИХ ГАРАНТИЙ;
даже без неявной гарантии ТОВАРНОГО ВИДА или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ.
Подробнее см. в Стандартной общественной лицензии GNU.
Вы должны были получить копию Стандартной общественной лицензии GNU вместе с этой программой.
Если это не так, см. <https://www.gnu.org/licenses/>.
"""

import zipfile
import json
import os
import shutil


def install_pkg(file_name):
    with zipfile.ZipFile(file_name) as zip_file:
        with zip_file.open('pkg_data.json') as data_file:
            pkg_meta_data = json.JSONDecoder().decode(data_file.read().decode())

        for file in zip_file.infolist():
            if file.filename.startswith('files/'):
                print(f'EXTRACT: {file.filename}')
                file.filename = 'pkg/' + pkg_meta_data['dir'] + file.filename.replace('files', '', 1)
                zip_file.extract(file)

    with open('pkglist.json') as file:
        print('READ: pkglist.json')
        pkg_list = json.JSONDecoder().decode(file.read())

    pkg_list[pkg_meta_data['name']] = {'dir': pkg_meta_data['dir'], 'info': pkg_meta_data['info']}

    with open('pkglist.json', 'w') as file:
        print('UPDATE: pkglist.json')
        file.write(json.JSONEncoder().encode(pkg_list))


def delete_pkg(pkg_name):
    with open('pkglist.json') as file:
        print('READ: pkglist.json')
        pkg_list = json.JSONDecoder().decode(file.read())

    print('DELETE: files')
    shutil.rmtree('./pkg/' + pkg_list[pkg_name]['dir'])
    del pkg_list[pkg_name]

    with open('pkglist.json', 'w') as file:
        print('UPDATE: pkglist.json')
        file.write(json.JSONEncoder().encode(pkg_list))


def main():
    while True:
        cmd = input('> ')
        if cmd == 'i':
            param = input('? ')
            install_pkg(param)
        elif cmd == 'd':
            param = input('? ')
            delete_pkg(param)
        elif cmd == 'q':
            break
        else:
            print('err')


if __name__ == '__main__':
    main()
