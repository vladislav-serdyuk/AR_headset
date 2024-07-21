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

import zipfile
import json
import shutil


def install_pkg(file_name: str, skip_question=False):
    with open('pkglist.json', encoding='utf-8') as file:
        print('READ: pkglist.json')
        pkg_list = json.JSONDecoder().decode(file.read())

    print(f'READ: {file_name}')
    with zipfile.ZipFile(file_name) as zip_file:
        print(f'READ: {file_name}/pkg_data.json')
        with zip_file.open('pkg_data.json') as data_file:
            pkg_meta_data: dict[str, str] = json.JSONDecoder().decode(data_file.read().decode())

            if pkg_meta_data['name'] in pkg_list:
                ask = 'u'
                if not skip_question:
                    ask = input('pkg is installed, update or cansel? u/c: ')
                if ask == 'u':
                    print('selected update pkg')
                    print('run deleting pkg')
                    delete_pkg(pkg_meta_data['name'])
                elif ask == 'c':
                    return
                else:
                    print('bad command: run "cansel"')
                    return

        for file in zip_file.infolist():
            if file.filename.startswith('files/'):
                print(f'EXTRACT: {file.filename}')
                file.filename = 'pkg/' + pkg_meta_data['dir'] + file.filename.replace('files', '', 1)
                zip_file.extract(file)

    pkg_list[pkg_meta_data['name']] = {'dir': pkg_meta_data['dir'], 'info': pkg_meta_data['info'],
                                       'description': pkg_meta_data.get('description', 'Unknown')}

    with open('pkglist.json', 'w') as file:
        print('UPDATE: pkglist.json')
        file.write(json.JSONEncoder().encode(pkg_list))

    print('install(update) pkg successful')


def delete_pkg(pkg_name: str):
    with open('pkglist.json', encoding='utf-8') as file:
        print('READ: pkglist.json')
        pkg_list = json.JSONDecoder().decode(file.read())

    print('DELETE: files')
    shutil.rmtree('./pkg/' + pkg_list[pkg_name]['dir'])
    del pkg_list[pkg_name]

    with open('pkglist.json', 'w') as file:
        print('UPDATE: pkglist.json')
        file.write(json.JSONEncoder().encode(pkg_list))
    print('delete pkg successful')


def main():
    while True:
        cmd = input('entry command: install, delete or quit? i/d/q > ')
        if cmd == 'i':
            param = input('entry file name ? ')
            install_pkg(param)
        elif cmd == 'd':
            param = input('entry pkg name ? ')
            delete_pkg(param)
        elif cmd == 'q':
            break
        else:
            print('bad command')


if __name__ == '__main__':
    main()
