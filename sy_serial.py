# -*- coding:utf-8 -*-

import os
import time

class sy_serial():
    def __init__(self):
        if os.name == 'nt':
            self.windows_init()

        if os.name == 'posix':
            self.linux_init()

    def windows_init(self):
        try:
            pass
        except ModuleNotFoundError:
            os.system('python3 -m pip install serial')
            print('installing serial...')
            time.sleep(120)
            try:
                pass
            except:
                print('damn...')

    def linux_init(self):
        try:
            import pty
        except:
            pass

    def serial_write_data(self, serial, _data):
        #   单行数据
        serial.write(bytes.fromhex('02'))
        for _c in _data:
            serial.write(_c.encode(encoding='utf-8'))
        serial.write(bytes.fromhex('03'))
