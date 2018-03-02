# -*- coding:utf-8 -*-

import datetime


class sy_date():
    @staticmethod
    def datetime_format(date=None, mode=1):
        """
        获取特定格式的日期时间字符串
        """
        if date is None:
            date = datetime.datetime.now()
        if mode == 1:
            return str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日'
        elif mode == 2:
            return date.strftime('%Y%m%d%H%M%S')
        elif mode == 3:
            return date.strftime('%m/%d/%Y')
        elif mode == 4:
            return str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日 ' + str(date.hour).zfill(
                2) + ':' + str(date.minute).zfill(2) + ':' + str(date.second).zfill(2)
        elif mode == 5:
            return date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return repr(date)


import logging, inspect, os
class sy_log():
    def get_logger(self, _name):

        logger = logging.getLogger(_name)

        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        if not os.path.exists(os.path.join(dirpath, 'log')):
            os.makedirs(os.path.join(dirpath, 'log'))
        handler = logging.FileHandler(os.path.join(dirpath, 'log', sy_date.datetime_format(mode=2) + ".log"))

        formatter = logging.Formatter('%(asctime)s %(name)-12s [line:%(lineno)d] %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger


import re
import sys
class sy_check():
    def check_ip(self, _str):
        return re.match(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", _str)

    def _check_py_version(self, _v=None):
        if _v is not None and sys.version.split(' ')[0] == _v:
            return True
        else:
            return False

if __name__ == '__main__':
    check = sy_check()
    print(check._check_py_version(_v='3.6.4'))

