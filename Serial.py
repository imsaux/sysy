# -*- coding:utf-8 -*-
# todo win10下还需适配
import os
import time
import multiprocessing

class sy_serial():
    def __init__(self):
        if os.name == 'nt':
            self.windows_init()

        if os.name == 'posix':
            self.linux_init()

    def windows_init(self):
        try:
            import _serial
        except ModuleNotFoundError:
            os.system('python3 -m pip install pyserial')
            print('installing pyserial...')
            time.sleep(120)
            try:
                import _serial
            except:
                print('damn...')

    def linux_init(self):
        try:
            import pty
        except ModuleNotFoundError:
            os.system('python3 -m pip install pty')

    def serial_write_data(self, serial, _data):
        #   单行数据
        serial.write(bytes.fromhex('02'))
        for _c in _data:
            serial.write(_c.encode(encoding='utf-8'))
        serial.write(bytes.fromhex('03'))
