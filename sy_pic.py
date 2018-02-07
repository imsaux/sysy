# -*- coding:utf-8 -*-

import PIL.Image
import os


class sy_pic():
    def __init__(self, file=None):
        self._img = None
        self._file = None
        if file is not None and os.path.exists(file):
            self._img = PIL.Image.open(file)
            self._file = file

    def get_info(self, file_name):
        return self._img.size[0], self._img.size[1], os.path.getsize(self._file)


    def zoom(self, mode, w_ratio=1.0, h_ratio=1.0):
        # 缩放图片
        if mode == 1: # 原图
            pass
        elif mode == 2: # 等比例缩放
            pass
        elif mode == 3: # 指定系数缩放
            pass

    def calc(self):
        pass